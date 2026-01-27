"""Stage-specific result models."""

from dataclasses import dataclass
from typing import Optional
from pydantic import BaseModel, Field


class SelectionResult(BaseModel):
    """Result from the Selection stage (Stage 2).

    Determines if a sentence contains verifiable content.
    """
    has_verifiable_content: bool = Field(
        description="Whether the sentence contains any verifiable content"
    )
    rewritten_sentence: Optional[str] = Field(
        default=None,
        description="Rewritten sentence with only verifiable content (if partially verifiable)"
    )
    reason: str = Field(
        description="Explanation for the decision"
    )


class DisambiguationResult(BaseModel):
    """Result from the Disambiguation stage (Stage 3).

    Resolves ambiguities in sentences.
    """
    is_ambiguous: bool = Field(
        description="Whether the sentence contains ambiguity"
    )
    can_be_disambiguated: bool = Field(
        description="Whether ambiguity can be resolved with context"
    )
    disambiguated_sentence: Optional[str] = Field(
        default=None,
        description="Disambiguated version of the sentence (if resolvable)"
    )
    ambiguity_explanation: str = Field(
        description="Explanation of the ambiguity and resolution attempt"
    )


class DecompositionResult(BaseModel):
    """Result from the Decomposition stage (Stage 4).

    Extracts atomic claims from sentences.
    """
    claims: list[str] = Field(
        description="List of extracted atomic claims"
    )
    extraction_reasoning: str = Field(
        description="Reasoning behind the claim extraction"
    )


# For backward compatibility and convenience
@dataclass
class StageResult:
    """Generic stage result wrapper."""
    success: bool
    data: Optional[BaseModel] = None
    error: Optional[str] = None
