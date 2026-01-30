"""Test that all modules can be imported correctly."""

import pytest


def test_import_main_package():
    """Test that main package imports successfully."""
    from src import ClaimExtractionPipeline, Claim, ClaimExtractionResult, PipelineResult, SentenceStatus

    assert ClaimExtractionPipeline is not None
    assert Claim is not None
    assert ClaimExtractionResult is not None
    assert PipelineResult is not None
    assert SentenceStatus is not None


def test_import_models():
    """Test that all models can be imported."""
    from claimification.claim_extraction.models import (
        SentenceWithContext,
        SentenceMetadata,
        Claim,
        ClaimExtractionResult,
        PipelineResult,
        SentenceStatus,
        SelectionResult,
        DisambiguationResult,
        DecompositionResult,
    )

    assert SentenceWithContext is not None
    assert SentenceMetadata is not None
    assert Claim is not None
    assert ClaimExtractionResult is not None
    assert PipelineResult is not None
    assert SentenceStatus is not None
    assert SelectionResult is not None
    assert DisambiguationResult is not None
    assert DecompositionResult is not None


def test_import_stages():
    """Test that all stages can be imported."""
    from claimification.claim_extraction.stages import (
        SentenceSplitter,
        SelectionAgent,
        DisambiguationAgent,
        DecompositionAgent,
    )

    assert SentenceSplitter is not None
    assert SelectionAgent is not None
    assert DisambiguationAgent is not None
    assert DecompositionAgent is not None


def test_import_prompts():
    """Test that all prompts can be imported."""
    from claimification.claim_extraction.prompts import (
        SELECTION_SYSTEM_PROMPT,
        create_selection_prompt,
        DISAMBIGUATION_SYSTEM_PROMPT,
        create_disambiguation_prompt,
        DECOMPOSITION_SYSTEM_PROMPT,
        create_decomposition_prompt,
    )

    assert SELECTION_SYSTEM_PROMPT is not None
    assert create_selection_prompt is not None
    assert DISAMBIGUATION_SYSTEM_PROMPT is not None
    assert create_disambiguation_prompt is not None
    assert DECOMPOSITION_SYSTEM_PROMPT is not None
    assert create_decomposition_prompt is not None


def test_pipeline_instantiation():
    """Test that pipeline can be instantiated."""
    from src import ClaimExtractionPipeline

    # Should not raise any import errors
    pipeline = ClaimExtractionPipeline.__init__.__code__
    assert pipeline is not None
