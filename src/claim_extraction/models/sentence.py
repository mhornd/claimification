"""Sentence data models for claim extraction pipeline."""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional


@dataclass
class SentenceWithContext:
    """A sentence with its surrounding context.

    Attributes:
        sentence_id: Unique identifier for the sentence
        text: The sentence text
        context: Surrounding context (previous/next sentences, headers, question)
        metadata: Additional metadata (position, headers, etc.)
    """
    sentence_id: str
    text: str
    context: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate sentence data."""
        if not self.text.strip():
            raise ValueError("Sentence text cannot be empty")
        if not self.sentence_id:
            raise ValueError("Sentence ID is required")


@dataclass
class SentenceMetadata:
    """Metadata for a sentence in the answer.

    Attributes:
        position: Index position in the original answer
        headers: Hierarchy of markdown headers (if applicable)
        paragraph: Paragraph number
        char_start: Character start position in original text
        char_end: Character end position in original text
    """
    position: int
    headers: list[str] = field(default_factory=list)
    paragraph: Optional[int] = None
    char_start: Optional[int] = None
    char_end: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "position": self.position,
            "headers": self.headers,
            "paragraph": self.paragraph,
            "char_start": self.char_start,
            "char_end": self.char_end
        }
