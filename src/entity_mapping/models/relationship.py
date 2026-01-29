"""Relationship data models for entity relationship mapping."""

from typing import Optional
from pydantic import BaseModel, Field, field_validator, model_validator


class Relationship(BaseModel):
    """Represents a relationship between two entities.

    Relationships can be explicit (directly stated in text) or
    inferred (derived through LLM reasoning).
    """

    source_entity_id: str = Field(
        ...,
        description="ID of the source entity"
    )

    target_entity_id: str = Field(
        ...,
        description="ID of the target entity"
    )

    relationship_type: str = Field(
        ...,
        description="Type of relationship (e.g., 'founded', 'works_at', 'located_in')"
    )

    evidence: str = Field(
        ...,
        description="Text span supporting this relationship"
    )

    is_inferred: bool = Field(
        default=False,
        description="False for explicit relationships, True for inferred"
    )

    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Confidence score (1.0 for explicit, <1.0 for inferred)"
    )

    reasoning: Optional[str] = Field(
        default=None,
        description="Explanation for inferred relationships"
    )

    @field_validator('confidence')
    @classmethod
    def validate_confidence(cls, v: float, info) -> float:
        """Ensure explicit relationships have confidence 1.0."""
        is_inferred = info.data.get('is_inferred', False)
        if not is_inferred and v != 1.0:
            raise ValueError("Explicit relationships must have confidence 1.0")
        return v

    @model_validator(mode='after')
    def validate_inferred_relationships(self):
        """Ensure inferred relationships have reasoning."""
        if self.is_inferred and not self.reasoning:
            raise ValueError("Inferred relationships must include reasoning")
        return self
