"""Stage 1: Sentence Splitting and Context Creation.

This stage splits the answer into individual sentences and creates
context for each sentence (surrounding sentences, headers, question).
"""

import re
from typing import List, Optional
from ..models import SentenceWithContext, SentenceMetadata


class SentenceSplitter:
    """Splits text into sentences and creates context for each."""

    def __init__(
        self,
        context_sentences_before: int = 2,
        context_sentences_after: int = 2,
        include_question: bool = True,
        include_headers: bool = True
    ):
        """Initialize sentence splitter.

        Args:
            context_sentences_before: Number of sentences to include before
            context_sentences_after: Number of sentences to include after
            include_question: Whether to include the question in context
            include_headers: Whether to include markdown headers in context
        """
        self.context_sentences_before = context_sentences_before
        self.context_sentences_after = context_sentences_after
        self.include_question = include_question
        self.include_headers = include_headers

    def split_and_create_context(
        self,
        question: str,
        answer: str
    ) -> List[SentenceWithContext]:
        """Split answer into sentences and create context for each.

        Args:
            question: The question that prompted the answer
            answer: The answer text to split

        Returns:
            List of SentenceWithContext objects
        """
        # Extract headers if markdown
        headers_map = self._extract_markdown_headers(
            answer) if self.include_headers else {}

        # Split into sentences
        sentences = self._split_into_sentences(answer)

        # Create context for each sentence
        results = []
        for i, sentence_text in enumerate(sentences):
            sentence_id = f"sent_{i:03d}"

            # Build context
            context = self._build_context(
                question=question,
                sentences=sentences,
                current_index=i,
                headers_map=headers_map
            )

            # Create metadata
            metadata = SentenceMetadata(
                position=i,
                headers=headers_map.get(i, []),
                paragraph=self._get_paragraph_number(answer, sentence_text)
            ).to_dict()

            results.append(SentenceWithContext(
                sentence_id=sentence_id,
                text=sentence_text,
                context=context,
                metadata=metadata
            ))

        return results

    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences using regex.

        Uses a simple but effective regex that handles:
        - Standard sentence endings (. ! ?)
        - Abbreviations (e.g., Dr., U.S.)
        - Multiple punctuation (e.g., ...)
        - Quoted sentences

        For production, consider using spaCy for more robust splitting.
        """
        # Remove multiple newlines
        text = re.sub(r'\n\s*\n', '\n', text)

        # Simple sentence splitting pattern
        # This is a simplified version - spaCy would be more robust
        pattern = r'(?<=[.!?])\s+(?=[A-Z])'
        sentences = re.split(pattern, text)

        # Clean up
        sentences = [s.strip() for s in sentences if s.strip()]

        # Handle markdown headers (keep them as separate "sentences")
        result = []
        for sent in sentences:
            if sent.startswith('#'):
                # This is a header, don't split it further
                result.append(sent)
            else:
                result.append(sent)

        return result

    def _build_context(
        self,
        question: str,
        sentences: List[str],
        current_index: int,
        headers_map: dict
    ) -> str:
        """Build context string for a sentence.

        Context includes:
        - The question (if enabled)
        - Surrounding sentences
        - Relevant headers
        """
        context_parts = []

        # Add question
        if self.include_question:
            context_parts.append(f"**Question:** {question}")

        # Add headers
        if self.include_headers and current_index in headers_map:
            headers = headers_map[current_index]
            if headers:
                context_parts.append(f"**Section:** {' > '.join(headers)}")

        # Add preceding sentences
        start_idx = max(0, current_index - self.context_sentences_before)
        if start_idx < current_index:
            preceding = " ".join(sentences[start_idx:current_index])
            context_parts.append(f"**Before:** {preceding}")

        # Add following sentences
        end_idx = min(len(sentences), current_index +
                      self.context_sentences_after + 1)
        if end_idx > current_index + 1:
            following = " ".join(sentences[current_index + 1:end_idx])
            context_parts.append(f"**After:** {following}")

        return "\n\n".join(context_parts)

    def _extract_markdown_headers(self, text: str) -> dict:
        """Extract markdown headers and map them to sentence indices.

        Returns a dict mapping sentence index to list of headers.
        """
        headers_map = {}
        current_headers = []
        lines = text.split('\n')

        sentence_idx = 0
        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Check if line is a markdown header
            header_match = re.match(r'^(#{1,6})\s+(.+)$', line)
            if header_match:
                level = len(header_match.group(1))
                header_text = header_match.group(2)

                # Update header hierarchy
                # Remove headers at same or deeper level
                current_headers = [h for h in current_headers if h[0] < level]
                current_headers.append((level, header_text))
            else:
                # Regular text - map current headers to this sentence
                if current_headers:
                    headers_map[sentence_idx] = [h[1] for h in current_headers]
                sentence_idx += 1

        return headers_map

    def _get_paragraph_number(self, full_text: str, sentence: str) -> Optional[int]:
        """Get paragraph number for a sentence (simple implementation)."""
        # Split by double newlines to get paragraphs
        paragraphs = re.split(r'\n\s*\n', full_text)
        for i, para in enumerate(paragraphs):
            if sentence in para:
                return i
        return None
