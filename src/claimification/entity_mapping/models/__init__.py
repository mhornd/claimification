"""Data models for entity relationship mapping."""

from claimification.entity_mapping.models.entity import Entity, EntityType
from claimification.entity_mapping.models.relationship import Relationship
from claimification.entity_mapping.models.knowledge_graph import (
    KnowledgeGraph,
    GraphMetadata
)

__all__ = [
    "Entity",
    "EntityType",
    "Relationship",
    "KnowledgeGraph",
    "GraphMetadata"
]
