"""Claimification - Extract verifiable factual claims and map entity relationships.

This package provides:
1. Claim Extraction - Multi-stage pipeline for extracting verifiable factual claims
2. Entity Mapping - Extract entities and relationships to build knowledge graphs
"""

from claimification.claim_extraction import (
    ClaimExtractionPipeline,
    Claim,
    PipelineResult,
    ClaimExtractionResult,
    SentenceStatus
)

from claimification.entity_mapping import (
    EntityMappingPipeline,
    Entity,
    EntityType,
    Relationship,
    KnowledgeGraph,
    GraphMetadata
)

__version__ = "2.1.0"
__author__ = "TwoDigits"

__all__ = [
    "ClaimExtractionPipeline",
    "Claim",
    "PipelineResult",
    "ClaimExtractionResult",
    "SentenceStatus",
    "EntityMappingPipeline",
    "Entity",
    "EntityType",
    "Relationship",
    "KnowledgeGraph",
    "GraphMetadata",
]
