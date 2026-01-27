"""Claim data models for Claimification pipeline."""

from dataclasses import dataclass, field
from typing import Literal, List, Dict, Any, Optional
from enum import Enum


class SentenceStatus(str, Enum):
    """Possible statuses for a sentence after processing."""
    EXTRACTED = "extracted"
    NO_VERIFIABLE_CLAIMS = "no_verifiable_claims"
    CANNOT_DISAMBIGUATE = "cannot_disambiguate"
    PROCESSING_ERROR = "processing_error"


@dataclass
class Claim:
    """A single extracted claim.

    Attributes:
        text: The claim text
        source_sentence_id: ID of the source sentence
        confidence: Optional confidence score (0-1)
    """
    text: str
    source_sentence_id: str
    confidence: Optional[float] = None

    def __post_init__(self):
        """Validate claim data."""
        if not self.text.strip():
            raise ValueError("Claim text cannot be empty")
        if self.confidence is not None:
            if not 0 <= self.confidence <= 1:
                raise ValueError("Confidence must be between 0 and 1")


@dataclass
class ClaimExtractionResult:
    """Result of claim extraction for a single sentence.

    Attributes:
        source_sentence: The original sentence text
        sentence_id: Unique identifier for the sentence
        status: Processing status
        claims: List of extracted claims (empty if status is not EXTRACTED)
        metadata: Additional information (reasoning, error details, etc.)
    """
    source_sentence: str
    sentence_id: str
    status: SentenceStatus
    claims: List[Claim] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate extraction result."""
        if self.status == SentenceStatus.EXTRACTED and not self.claims:
            raise ValueError("Status is EXTRACTED but no claims provided")


@dataclass
class PipelineResult:
    """Complete result from the Claimification pipeline.

    Attributes:
        question: The original question
        answer: The original answer text
        sentence_results: Results for each processed sentence
        statistics: Pipeline execution statistics
    """
    question: str
    answer: str
    sentence_results: List[ClaimExtractionResult]
    statistics: Dict[str, Any] = field(default_factory=dict)

    def get_all_claims(self) -> List[Claim]:
        """Get all successfully extracted claims."""
        claims = []
        for result in self.sentence_results:
            if result.status == SentenceStatus.EXTRACTED:
                claims.extend(result.claims)
        return claims

    def get_statistics_summary(self) -> Dict[str, int]:
        """Get summary statistics of the extraction."""
        total_sentences = len(self.sentence_results)
        total_claims = len(self.get_all_claims())

        status_counts = {
            "extracted": 0,
            "no_verifiable_claims": 0,
            "cannot_disambiguate": 0,
            "processing_error": 0
        }

        for result in self.sentence_results:
            status_counts[result.status.value] += 1

        return {
            "total_sentences": total_sentences,
            "total_claims": total_claims,
            **status_counts
        }
