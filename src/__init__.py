"""Backward compatibility shim for old 'src' imports.

DEPRECATED: Import from 'claimification' instead.
"""

import warnings

warnings.warn(
    "Importing from 'src' is deprecated and will be removed in version 3.0. "
    "Please update imports to use 'claimification' instead:\n"
    "  from claimification.claim_extraction import ClaimExtractionPipeline\n"
    "  from claimification.entity_mapping import EntityMappingPipeline",
    DeprecationWarning,
    stacklevel=2
)

# Re-export from new location for backward compatibility
from claimification import *  # noqa: F401, F403

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
