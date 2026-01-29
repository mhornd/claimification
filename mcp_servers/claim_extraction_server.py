#!/usr/bin/env python3
"""Claim Extraction MCP Server - STDIO-based integration for Claude Code."""

import os
import sys
import json
import asyncio
from typing import Any

# MCP SDK imports
from mcp.server import Server
from mcp.types import Tool, TextContent

# Claim Extraction imports
from src.claim_extraction.pipeline import ClaimExtractionPipeline
from src.claim_extraction.models import PipelineResult


# Initialize server
server = Server("claim-extraction")


def format_result_as_markdown(result: PipelineResult) -> str:
    """Format PipelineResult as readable markdown.

    Args:
        result: The pipeline result to format

    Returns:
        Formatted markdown string
    """
    stats = result.get_statistics_summary()
    claims = result.get_all_claims()

    output_lines = ["# Claim Extraction Results\n"]

    # Statistics summary
    output_lines.append("## Summary")
    output_lines.append(f"- **Total sentences:** {stats['total_sentences']}")
    output_lines.append(f"- **Claims extracted:** {stats['total_claims']}")
    output_lines.append(f"- **Processing time:** {result.statistics.get('total_time_seconds', 'N/A')}s")
    output_lines.append(f"- **Model used:** {result.statistics.get('model_used', 'N/A')}")
    output_lines.append("")

    # Extracted claims
    if claims:
        output_lines.append("## Extracted Claims\n")
        for i, claim in enumerate(claims, 1):
            output_lines.append(f"{i}. {claim.text}")
        output_lines.append("")
    else:
        output_lines.append("## Extracted Claims\n")
        output_lines.append("*No verifiable claims found in the text.*\n")

    # Status breakdown
    if stats['no_verifiable_claims'] > 0 or stats['cannot_disambiguate'] > 0 or stats['processing_error'] > 0:
        output_lines.append("## Processing Details\n")
        if stats['no_verifiable_claims'] > 0:
            output_lines.append(f"- **No verifiable claims:** {stats['no_verifiable_claims']} sentences")
        if stats['cannot_disambiguate'] > 0:
            output_lines.append(f"- **Cannot disambiguate:** {stats['cannot_disambiguate']} sentences")
        if stats['processing_error'] > 0:
            output_lines.append(f"- **Processing errors:** {stats['processing_error']} sentences")
        output_lines.append("")

    # Detailed sentence results (if needed)
    output_lines.append("## Detailed Results\n")
    for i, sent_result in enumerate(result.sentence_results, 1):
        output_lines.append(f"### Sentence {i}")
        output_lines.append(f"**Source:** {sent_result.source_sentence}\n")
        output_lines.append(f"**Status:** `{sent_result.status.value}`\n")

        if sent_result.claims:
            output_lines.append("**Extracted claims:**")
            for claim in sent_result.claims:
                output_lines.append(f"- {claim.text}")
            output_lines.append("")
        elif sent_result.metadata:
            # Show reason if no claims
            reason = sent_result.metadata.get('reason') or sent_result.metadata.get('ambiguity_explanation')
            if reason:
                output_lines.append(f"**Reason:** {reason}\n")

    return "\n".join(output_lines)


def validate_input(text: str) -> None:
    """Validate input text.

    Args:
        text: Input text to validate

    Raises:
        ValueError: If validation fails
    """
    if not text or len(text.strip()) == 0:
        raise ValueError("Text cannot be empty")
    if len(text) > 50000:  # ~50KB limit
        raise ValueError("Text too long (max 50,000 characters)")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="extract_claims",
            description=(
                "Extract verifiable factual claims from text using a sophisticated 4-stage pipeline. "
                "The pipeline: (1) splits text into sentences, (2) detects verifiable content, "
                "(3) resolves ambiguities, and (4) extracts atomic claims. "
                "Based on research from Microsoft Research (Metropolitansky & Larson, 2025)."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to extract claims from (max 50,000 characters)"
                    },
                    "question": {
                        "type": "string",
                        "description": "Optional question for additional context (backward compatibility)"
                    },
                    "model": {
                        "type": "string",
                        "description": "Optional LLM model to use (default: gpt-5-nano-2025-08-07)",
                        "default": "gpt-5-nano-2025-08-07"
                    }
                },
                "required": ["text"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Handle tool calls.

    Args:
        name: Tool name
        arguments: Tool arguments

    Returns:
        List of TextContent responses
    """
    if name != "extract_claims":
        raise ValueError(f"Unknown tool: {name}")

    try:
        # Extract arguments
        text = arguments.get("text", "")
        question = arguments.get("question")
        model = arguments.get("model", os.getenv("CLAIMIFICATION_MODEL", "gpt-5-nano-2025-08-07"))

        # Validate input
        validate_input(text)

        # Initialize pipeline (with verbose=False for MCP)
        pipeline = ClaimExtractionPipeline(
            model=model,
            temperature=0.0,
            verbose=False  # No console output in MCP mode
        )

        # Run extraction
        result: PipelineResult = pipeline.extract_claims(
            text=text,
            question=question
        )

        # Format result
        formatted_output = format_result_as_markdown(result)

        return [
            TextContent(
                type="text",
                text=formatted_output
            )
        ]

    except Exception as e:
        # Return error as formatted text
        error_output = f"""# Claim Extraction Error

**Error:** {str(e)}

**Suggestions:**
- Check that your API key (OPENAI_API_KEY or ANTHROPIC_API_KEY) is set in .env
- Ensure the input text is not empty and under 50,000 characters
- Verify your API key has sufficient credits
- Try a different model if the current one is unavailable

**Need help?** Check the documentation at https://github.com/mhornd/claimification
"""
        return [
            TextContent(
                type="text",
                text=error_output
            )
        ]


async def main():
    """Main entry point for the MCP server."""
    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
