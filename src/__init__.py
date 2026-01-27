"""Claimification - Extract verifiable factual claims from LLM outputs.

This package provides a multi-stage pipeline for extracting and validating
factual claims from question-answer pairs.
"""

from .pipeline import ClaimificationPipeline
from .models import (
    Claim,
    ClaimExtractionResult,
    PipelineResult,
    SentenceStatus
)

__version__ = "1.0.0"
__author__ = "TwoDigits"

__all__ = [
    "ClaimificationPipeline",
    "Claim",
    "ClaimExtractionResult",
    "PipelineResult",
    "SentenceStatus",
]
