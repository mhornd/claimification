#!/usr/bin/env python3
"""Entity Mapping MCP Server - STDIO-based integration for Claude Code."""

import os
import sys
import json
import asyncio
from typing import Any

# MCP SDK imports
from mcp.server import Server
from mcp.types import Tool, TextContent

# Entity mapping imports
from src.entity_mapping import EntityMappingPipeline, KnowledgeGraph


# Initialize server
server = Server("entity-mapping")


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
            name="extract_entities_and_relationships",
            description=(
                "Extract entities and relationships from unstructured text using a 3-stage pipeline. "
                "Stage 1: Entity extraction with coreference resolution. "
                "Stage 2: Explicit relationship extraction. "
                "Stage 3: Implicit relationship inference using LLM reasoning. "
                "Returns a knowledge graph with both JSON and natural language summary."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to analyze (max 50,000 characters)"
                    },
                    "context": {
                        "type": "string",
                        "description": "Optional contextual information (e.g., original question)"
                    },
                    "model": {
                        "type": "string",
                        "description": "Optional LLM model to use (default: gpt-5-nano-2025-08-07)",
                        "default": "gpt-5-nano-2025-08-07"
                    },
                    "include_inferred": {
                        "type": "boolean",
                        "description": "Whether to include inferred relationships (default: true)",
                        "default": True
                    },
                    "confidence_threshold": {
                        "type": "number",
                        "description": "Minimum confidence for inferred relationships (default: 0.7)",
                        "default": 0.7,
                        "minimum": 0.0,
                        "maximum": 1.0
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
    if name != "extract_entities_and_relationships":
        raise ValueError(f"Unknown tool: {name}")

    try:
        # Extract arguments
        text = arguments.get("text", "")
        context = arguments.get("context")
        model = arguments.get("model", os.getenv("ENTITY_MAPPING_MODEL", "gpt-5-nano-2025-08-07"))
        include_inferred = arguments.get("include_inferred", True)
        confidence_threshold = arguments.get("confidence_threshold", 0.7)

        # Validate input
        validate_input(text)

        # Initialize pipeline
        pipeline = EntityMappingPipeline(
            model=model,
            temperature=0.0,
            confidence_threshold=confidence_threshold,
            include_inferred=include_inferred
        )

        # Extract knowledge graph
        knowledge_graph: KnowledgeGraph = pipeline.extract_knowledge_graph(
            text=text,
            context=context
        )

        # Format output as markdown with both summary and JSON
        output_lines = ["# Entity Relationship Mapping Results\n"]

        # Natural language summary
        output_lines.append("## Summary\n")
        output_lines.append(knowledge_graph.to_summary())
        output_lines.append("\n")

        # Metadata
        output_lines.append("## Metadata\n")
        output_lines.append(f"- **Model used:** {knowledge_graph.metadata.model_used}")
        output_lines.append(f"- **Total entities:** {knowledge_graph.metadata.total_entities}")
        output_lines.append(f"- **Total relationships:** {knowledge_graph.metadata.total_relationships}")
        output_lines.append(f"- **Explicit relationships:** {knowledge_graph.metadata.explicit_relationships}")
        output_lines.append(f"- **Inferred relationships:** {knowledge_graph.metadata.inferred_relationships}")
        output_lines.append(f"- **Created at:** {knowledge_graph.metadata.created_at}")
        output_lines.append("\n")

        # JSON export
        output_lines.append("## JSON Export\n")
        output_lines.append("```json")
        output_lines.append(json.dumps(knowledge_graph.to_json(), indent=2))
        output_lines.append("```\n")

        formatted_output = "\n".join(output_lines)

        return [
            TextContent(
                type="text",
                text=formatted_output
            )
        ]

    except Exception as e:
        # Return error as formatted text
        error_output = f"""# Entity Mapping Error

**Error:** {str(e)}

**Suggestions:**
- Check that your API key (OPENAI_API_KEY or ANTHROPIC_API_KEY) is set
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
