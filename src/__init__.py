"""Claimification - Extract verifiable factual claims and map entity relationships.

This package provides:
1. Claim Extraction - Multi-stage pipeline for extracting verifiable factual claims
2. Entity Mapping - Extract entities and relationships to build knowledge graphs
"""

from src.claim_extraction import (
    ClaimificationPipeline,
    Claim,
    PipelineResult,
    ClaimExtractionResult,
    SentenceStatus
)

__version__ = "2.0.0"
__author__ = "TwoDigits"

__all__ = [
    "ClaimificationPipeline",
    "Claim",
    "PipelineResult",
    "ClaimExtractionResult",
    "SentenceStatus",
]
