"""Entity data models for entity relationship mapping."""

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class EntityType(str, Enum):
    """Types of entities that can be extracted."""

    PERSON = "PERSON"
    ORGANIZATION = "ORGANIZATION"
    LOCATION = "LOCATION"
    PRODUCT = "PRODUCT"
    EVENT = "EVENT"
    CONCEPT = "CONCEPT"
    DATE = "DATE"
    OTHER = "OTHER"


class Entity(BaseModel):
    """Represents an extracted entity with metadata.

    An entity is a canonical representation of a real-world object
    mentioned in the text, with all its textual mentions tracked.
    """

    id: str = Field(
        ...,
        description="Unique identifier (e.g., 'e1', 'e2')"
    )

    text: str = Field(
        ...,
        description="Canonical form of the entity (e.g., 'Sarah Johnson')"
    )

    type: EntityType = Field(
        ...,
        description="Classification of the entity"
    )

    mentions: List[str] = Field(
        default_factory=list,
        description="All text spans referring to this entity (e.g., ['Sarah', 'she', 'the founder'])"
    )

    context: Optional[str] = Field(
        default=None,
        description="Surrounding sentence for disambiguation"
    )

    class Config:
        """Pydantic config."""
        use_enum_values = True
