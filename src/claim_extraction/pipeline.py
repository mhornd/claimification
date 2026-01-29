"""Claim Extraction Pipeline - Orchestrates all stages."""

import time
from typing import Optional
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from .models import (
    SentenceWithContext,
    Claim,
    ClaimExtractionResult,
    PipelineResult,
    SentenceStatus,
    SelectionResult,
    DisambiguationResult,
    DecompositionResult
)
from .stages.sentence_splitter import SentenceSplitter
from .stages.selection_agent import SelectionAgent
from .stages.disambiguation_agent import DisambiguationAgent
from .stages.decomposition_agent import DecompositionAgent


class ClaimExtractionPipeline:
    """Main pipeline for extracting factual claims from text."""

    def __init__(
        self,
        model: str = "gpt-5-nano-2025-08-07",
        temperature: float = 0.0,
        context_sentences: int = 2,
        verbose: bool = True
    ):
        """Initialize the claim extraction pipeline.

        Args:
            model: LLM model to use for agents
            temperature: Temperature for LLM (0.0 = deterministic)
            context_sentences: Number of surrounding sentences for context
            verbose: Whether to print progress messages
        """
        self.verbose = verbose
        self.console = Console() if verbose else None

        # Initialize stages
        self.sentence_splitter = SentenceSplitter(
            context_sentences_before=context_sentences,
            context_sentences_after=context_sentences
        )
        self.selection_agent = SelectionAgent(
            model=model, temperature=temperature)
        self.disambiguation_agent = DisambiguationAgent(
            model=model, temperature=temperature)
        self.decomposition_agent = DecompositionAgent(
            model=model, temperature=temperature)

    def extract_claims(self, text: str, question: Optional[str] = None) -> PipelineResult:
        """Extract claims from text.

        Args:
            text: The text to extract claims from
            question: Optional question for context (for backward compatibility)

        Returns:
            PipelineResult containing all extracted claims and metadata
        """
        start_time = time.time()

        if self.verbose:
            self.console.print(
                "\n[bold cyan]Starting Claim Extraction Pipeline[/bold cyan]")
            if question:
                self.console.print(f"Question: {question[:100]}...")
            self.console.print(f"Text length: {len(text)} characters\n")

        # Stage 1: Split into sentences and create context
        if self.verbose:
            self.console.print(
                "[bold]Stage 1:[/bold] Splitting into sentences...")

        sentences = self.sentence_splitter.split_and_create_context(
            text, question)

        if self.verbose:
            self.console.print(f"  ✓ Found {len(sentences)} sentences\n")

        # Process each sentence through stages 2-4
        sentence_results = []

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
            disable=not self.verbose
        ) as progress:
            task = progress.add_task(
                f"Processing sentences...",
                total=len(sentences)
            )

            for i, sentence_obj in enumerate(sentences):
                progress.update(
                    task,
                    description=f"Processing sentence {i+1}/{len(sentences)}...",
                    advance=1
                )

                result = self._process_sentence(sentence_obj)
                sentence_results.append(result)

        # Calculate statistics
        end_time = time.time()
        statistics = {
            "total_time_seconds": round(end_time - start_time, 2),
            "sentences_processed": len(sentences),
            "model_used": self.selection_agent.model_name
        }

        pipeline_result = PipelineResult(
            text=text,
            sentence_results=sentence_results,
            statistics=statistics,
            question=question
        )

        # Print summary
        if self.verbose:
            self._print_summary(pipeline_result)

        return pipeline_result

    def _process_sentence(self, sentence: SentenceWithContext) -> ClaimExtractionResult:
        """Process a single sentence through stages 2-4.

        Args:
            sentence: SentenceWithContext object

        Returns:
            ClaimExtractionResult for this sentence
        """
        # Stage 2: Selection (Verifiable content detection)
        selection_result = self.selection_agent.process(
            sentence.text,
            sentence.context
        )

        if not selection_result.success:
            return ClaimExtractionResult(
                source_sentence=sentence.text,
                sentence_id=sentence.sentence_id,
                status=SentenceStatus.PROCESSING_ERROR,
                metadata={"error": selection_result.error}
            )

        selection_data: SelectionResult = selection_result.data

        # If no verifiable content, stop here
        if not selection_data.has_verifiable_content:
            return ClaimExtractionResult(
                source_sentence=sentence.text,
                sentence_id=sentence.sentence_id,
                status=SentenceStatus.NO_VERIFIABLE_CLAIMS,
                metadata={
                    "reason": selection_data.reason
                }
            )

        # Use rewritten sentence if available, otherwise original
        sentence_to_process = (
            selection_data.rewritten_sentence
            if selection_data.rewritten_sentence
            else sentence.text
        )

        # Stage 3: Disambiguation
        disambiguation_result = self.disambiguation_agent.process(
            sentence_to_process,
            sentence.context
        )

        if not disambiguation_result.success:
            return ClaimExtractionResult(
                source_sentence=sentence.text,
                sentence_id=sentence.sentence_id,
                status=SentenceStatus.PROCESSING_ERROR,
                metadata={"error": disambiguation_result.error}
            )

        disambiguation_data: DisambiguationResult = disambiguation_result.data

        # If ambiguous and cannot be disambiguated, stop here
        if disambiguation_data.is_ambiguous and not disambiguation_data.can_be_disambiguated:
            return ClaimExtractionResult(
                source_sentence=sentence.text,
                sentence_id=sentence.sentence_id,
                status=SentenceStatus.CANNOT_DISAMBIGUATE,
                metadata={
                    "ambiguity_explanation": disambiguation_data.ambiguity_explanation
                }
            )

        # Use disambiguated sentence if available
        final_sentence = (
            disambiguation_data.disambiguated_sentence
            if disambiguation_data.disambiguated_sentence
            else sentence_to_process
        )

        # Stage 4: Decomposition (Claim extraction)
        decomposition_result = self.decomposition_agent.process(
            final_sentence,
            sentence.context
        )

        if not decomposition_result.success:
            return ClaimExtractionResult(
                source_sentence=sentence.text,
                sentence_id=sentence.sentence_id,
                status=SentenceStatus.PROCESSING_ERROR,
                metadata={"error": decomposition_result.error}
            )

        decomposition_data: DecompositionResult = decomposition_result.data

        # If no claims extracted, mark as no verifiable claims
        if not decomposition_data.claims:
            return ClaimExtractionResult(
                source_sentence=sentence.text,
                sentence_id=sentence.sentence_id,
                status=SentenceStatus.NO_VERIFIABLE_CLAIMS,
                metadata={
                    "reasoning": decomposition_data.extraction_reasoning
                }
            )

        # Success - claims extracted
        claims = [
            Claim(
                text=claim_text,
                source_sentence_id=sentence.sentence_id
            )
            for claim_text in decomposition_data.claims
        ]

        return ClaimExtractionResult(
            source_sentence=sentence.text,
            sentence_id=sentence.sentence_id,
            status=SentenceStatus.EXTRACTED,
            claims=claims,
            metadata={
                "reasoning": decomposition_data.extraction_reasoning,
                "was_rewritten": selection_data.rewritten_sentence is not None,
                "was_disambiguated": disambiguation_data.disambiguated_sentence is not None
            }
        )

    def _print_summary(self, result: PipelineResult):
        """Print a summary of the pipeline results."""
        stats = result.get_statistics_summary()

        self.console.print("\n[bold green]Pipeline Complete![/bold green]")
        self.console.print(
            f"⏱️  Time: {result.statistics['total_time_seconds']}s")
        self.console.print(f"📝 Sentences: {stats['total_sentences']}")
        self.console.print(f"✅ Claims extracted: {stats['total_claims']}")
        self.console.print(
            f"❌ No verifiable claims: {stats['no_verifiable_claims']}")
        self.console.print(
            f"⚠️  Cannot disambiguate: {stats['cannot_disambiguate']}")

        if stats['processing_error'] > 0:
            self.console.print(f"🔴 Errors: {stats['processing_error']}")
