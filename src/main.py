"""Main entry point for Claimification."""

import os
import json
import argparse
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown

from .pipeline import ClaimificationPipeline
from .models import PipelineResult, SentenceStatus


# Load environment variables
load_dotenv()


def format_results_markdown(result: PipelineResult) -> str:
    """Format pipeline results as markdown.

    Args:
        result: PipelineResult to format

    Returns:
        Markdown-formatted string
    """
    md_lines = ["# Claim Extraction Results\n"]

    # Question and Answer
    md_lines.append(f"**Question:** {result.question}\n")
    md_lines.append(f"**Answer:** {result.answer[:200]}{'...' if len(result.answer) > 200 else ''}\n")

    # Statistics
    stats = result.get_statistics_summary()
    md_lines.append("## Summary Statistics\n")
    md_lines.append(f"- Total sentences: {stats['total_sentences']}")
    md_lines.append(f"- Total claims extracted: {stats['total_claims']}")
    md_lines.append(f"- Sentences with claims: {stats['extracted']}")
    md_lines.append(f"- No verifiable claims: {stats['no_verifiable_claims']}")
    md_lines.append(f"- Cannot disambiguate: {stats['cannot_disambiguate']}")
    if stats['processing_error'] > 0:
        md_lines.append(f"- Processing errors: {stats['processing_error']}")
    md_lines.append("")

    # Extracted Claims
    md_lines.append("## Extracted Claims\n")

    for i, sentence_result in enumerate(result.sentence_results):
        letter = chr(65 + i)  # A, B, C, ...

        md_lines.append(f"### {letter}. {sentence_result.source_sentence}\n")

        if sentence_result.status == SentenceStatus.EXTRACTED:
            for j, claim in enumerate(sentence_result.claims, 1):
                md_lines.append(f"{j}. {claim.text}")
            md_lines.append("")
        elif sentence_result.status == SentenceStatus.NO_VERIFIABLE_CLAIMS:
            md_lines.append("*❌ No verifiable claims*\n")
        elif sentence_result.status == SentenceStatus.CANNOT_DISAMBIGUATE:
            explanation = sentence_result.metadata.get('ambiguity_explanation', 'Unknown')
            md_lines.append(f"*⚠️ Cannot be disambiguated: {explanation}*\n")
        elif sentence_result.status == SentenceStatus.PROCESSING_ERROR:
            error = sentence_result.metadata.get('error', 'Unknown error')
            md_lines.append(f"*🔴 Processing error: {error}*\n")

    return "\n".join(md_lines)


def format_results_json(result: PipelineResult) -> str:
    """Format pipeline results as JSON.

    Args:
        result: PipelineResult to format

    Returns:
        JSON string
    """
    output = {
        "question": result.question,
        "answer": result.answer,
        "statistics": result.get_statistics_summary(),
        "sentences": []
    }

    for sentence_result in result.sentence_results:
        sentence_data = {
            "sentence_id": sentence_result.sentence_id,
            "source_sentence": sentence_result.source_sentence,
            "status": sentence_result.status.value,
            "claims": [claim.text for claim in sentence_result.claims],
            "metadata": sentence_result.metadata
        }
        output["sentences"].append(sentence_data)

    return json.dumps(output, indent=2, ensure_ascii=False)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Extract factual claims from question-answer pairs"
    )
    parser.add_argument(
        "--question",
        "-q",
        type=str,
        required=True,
        help="The question that prompted the answer"
    )
    parser.add_argument(
        "--answer",
        "-a",
        type=str,
        help="The answer text (or use --answer-file)"
    )
    parser.add_argument(
        "--answer-file",
        type=Path,
        help="Path to file containing the answer"
    )
    parser.add_argument(
        "--model",
        type=str,
        default=os.getenv("CLAIMIFICATION_MODEL", "gpt-4o"),
        help="LLM model to use (default: gpt-4o)"
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=float(os.getenv("CLAIMIFICATION_TEMPERATURE", "0.0")),
        help="LLM temperature (default: 0.0)"
    )
    parser.add_argument(
        "--context-sentences",
        type=int,
        default=int(os.getenv("CLAIMIFICATION_CONTEXT_SENTENCES", "2")),
        help="Number of surrounding sentences for context (default: 2)"
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        help="Output file path (default: stdout)"
    )
    parser.add_argument(
        "--format",
        choices=["markdown", "json"],
        default="markdown",
        help="Output format (default: markdown)"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress progress output"
    )

    args = parser.parse_args()

    # Get answer text
    if args.answer:
        answer_text = args.answer
    elif args.answer_file:
        answer_text = args.answer_file.read_text(encoding="utf-8")
    else:
        parser.error("Either --answer or --answer-file must be provided")

    # Initialize pipeline
    pipeline = ClaimificationPipeline(
        model=args.model,
        temperature=args.temperature,
        context_sentences=args.context_sentences,
        verbose=not args.quiet
    )

    # Extract claims
    result = pipeline.extract_claims(
        question=args.question,
        answer=answer_text
    )

    # Format output
    if args.format == "markdown":
        output_text = format_results_markdown(result)
    else:
        output_text = format_results_json(result)

    # Write or print output
    if args.output:
        args.output.write_text(output_text, encoding="utf-8")
        if not args.quiet:
            console = Console()
            console.print(f"\n[green]Results written to {args.output}[/green]")
    else:
        console = Console()
        if args.format == "markdown":
            console.print(Markdown(output_text))
        else:
            console.print(output_text)


if __name__ == "__main__":
    main()
