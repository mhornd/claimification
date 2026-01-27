"""Test data models."""

import pytest
from src.models import (
    Claim,
    SentenceStatus,
    ClaimExtractionResult,
    SentenceWithContext,
    SentenceMetadata,
)


def test_claim_creation():
    """Test Claim model creation."""
    claim = Claim(
        text="Argentina has inflation.",
        source_sentence_id="sent_001"
    )

    assert claim.text == "Argentina has inflation."
    assert claim.source_sentence_id == "sent_001"
    assert claim.confidence is None


def test_claim_with_confidence():
    """Test Claim with confidence score."""
    claim = Claim(
        text="Test claim",
        source_sentence_id="sent_001",
        confidence=0.95
    )

    assert claim.confidence == 0.95


def test_claim_empty_text_raises_error():
    """Test that empty claim text raises ValueError."""
    with pytest.raises(ValueError, match="Claim text cannot be empty"):
        Claim(text="", source_sentence_id="sent_001")


def test_claim_invalid_confidence_raises_error():
    """Test that invalid confidence raises ValueError."""
    with pytest.raises(ValueError, match="Confidence must be between 0 and 1"):
        Claim(text="Test", source_sentence_id="sent_001", confidence=1.5)


def test_sentence_with_context_creation():
    """Test SentenceWithContext creation."""
    sentence = SentenceWithContext(
        sentence_id="sent_001",
        text="Argentina has inflation.",
        context="Question: What are the challenges?"
    )

    assert sentence.sentence_id == "sent_001"
    assert sentence.text == "Argentina has inflation."
    assert sentence.context == "Question: What are the challenges?"


def test_sentence_empty_text_raises_error():
    """Test that empty sentence text raises ValueError."""
    with pytest.raises(ValueError, match="Sentence text cannot be empty"):
        SentenceWithContext(
            sentence_id="sent_001",
            text="",
            context="Some context"
        )


def test_claim_extraction_result_creation():
    """Test ClaimExtractionResult creation."""
    claims = [
        Claim(text="Claim 1", source_sentence_id="sent_001"),
        Claim(text="Claim 2", source_sentence_id="sent_001"),
    ]

    result = ClaimExtractionResult(
        source_sentence="Original sentence",
        sentence_id="sent_001",
        status=SentenceStatus.EXTRACTED,
        claims=claims
    )

    assert result.status == SentenceStatus.EXTRACTED
    assert len(result.claims) == 2
    assert result.claims[0].text == "Claim 1"


def test_claim_extraction_result_invalid_status():
    """Test that EXTRACTED status without claims raises error."""
    with pytest.raises(ValueError, match="Status is EXTRACTED but no claims provided"):
        ClaimExtractionResult(
            source_sentence="Test",
            sentence_id="sent_001",
            status=SentenceStatus.EXTRACTED,
            claims=[]  # Empty claims with EXTRACTED status
        )


def test_sentence_metadata_creation():
    """Test SentenceMetadata creation."""
    metadata = SentenceMetadata(
        position=0,
        headers=["Section 1", "Subsection 1.1"],
        paragraph=0
    )

    assert metadata.position == 0
    assert len(metadata.headers) == 2
    assert metadata.paragraph == 0


def test_sentence_metadata_to_dict():
    """Test SentenceMetadata to_dict conversion."""
    metadata = SentenceMetadata(
        position=5,
        headers=["Header"],
        paragraph=2,
        char_start=100,
        char_end=200
    )

    result = metadata.to_dict()

    assert result["position"] == 5
    assert result["headers"] == ["Header"]
    assert result["paragraph"] == 2
    assert result["char_start"] == 100
    assert result["char_end"] == 200
