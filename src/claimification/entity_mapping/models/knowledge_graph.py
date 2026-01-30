"""Knowledge graph data model."""

from typing import List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

from claimification.entity_mapping.models.entity import Entity
from claimification.entity_mapping.models.relationship import Relationship


class GraphMetadata(BaseModel):
    """Metadata about graph generation."""

    created_at: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat(),
        description="ISO timestamp of graph creation"
    )

    model_used: str = Field(
        ...,
        description="LLM model used for extraction"
    )

    total_entities: int = Field(
        ...,
        description="Total number of entities extracted"
    )

    total_relationships: int = Field(
        ...,
        description="Total number of relationships extracted"
    )

    explicit_relationships: int = Field(
        ...,
        description="Number of explicit relationships"
    )

    inferred_relationships: int = Field(
        ...,
        description="Number of inferred relationships"
    )


class KnowledgeGraph(BaseModel):
    """Represents a complete knowledge graph extracted from text.

    Contains entities, relationships, and methods to export in
    various formats (JSON, natural language summary).
    """

    entities: List[Entity] = Field(
        default_factory=list,
        description="List of extracted entities"
    )

    relationships: List[Relationship] = Field(
        default_factory=list,
        description="List of relationships between entities"
    )

    metadata: GraphMetadata = Field(
        ...,
        description="Metadata about graph generation"
    )

    def to_json(self) -> Dict[str, Any]:
        """Export as JSON dictionary.

        Returns:
            Dictionary representation of the knowledge graph
        """
        return {
            "entities": [entity.model_dump() for entity in self.entities],
            "relationships": [rel.model_dump() for rel in self.relationships],
            "metadata": self.metadata.model_dump()
        }

    def to_summary(self) -> str:
        """Generate natural language summary of the knowledge graph.

        Returns:
            Human-readable text description
        """
        lines = []

        # Entity summary
        entity_count = len(self.entities)
        if entity_count == 0:
            lines.append("The text contains no identifiable entities.")
            return "\n".join(lines)

        lines.append(f"The text describes {entity_count} entities:")
        for entity in self.entities:
            lines.append(f"- {entity.text} ({entity.type})")
        lines.append("")

        # Relationship summary
        explicit_rels = [r for r in self.relationships if not r.is_inferred]
        inferred_rels = [r for r in self.relationships if r.is_inferred]

        if explicit_rels:
            lines.append(f"Explicit relationships ({len(explicit_rels)}):")
            for i, rel in enumerate(explicit_rels, 1):
                source = self._get_entity_text(rel.source_entity_id)
                target = self._get_entity_text(rel.target_entity_id)
                lines.append(f"{i}. {source} {rel.relationship_type} {target}")
            lines.append("")

        if inferred_rels:
            lines.append(f"Inferred relationships ({len(inferred_rels)}):")
            for i, rel in enumerate(inferred_rels, 1):
                source = self._get_entity_text(rel.source_entity_id)
                target = self._get_entity_text(rel.target_entity_id)
                lines.append(
                    f"{i}. {source} {rel.relationship_type} {target} "
                    f"(confidence: {rel.confidence:.2f})"
                )
                lines.append(f"   → {rel.reasoning}")
            lines.append("")

        if not explicit_rels and not inferred_rels:
            lines.append("No relationships identified between entities.")

        return "\n".join(lines)

    def _get_entity_text(self, entity_id: str) -> str:
        """Helper to get entity text by ID.

        Args:
            entity_id: Entity ID to look up

        Returns:
            Entity canonical text, or ID if not found
        """
        for entity in self.entities:
            if entity.id == entity_id:
                return entity.text
        return entity_id  # Fallback
