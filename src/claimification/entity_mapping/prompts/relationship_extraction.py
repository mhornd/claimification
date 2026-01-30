"""Prompts for explicit relationship extraction stage."""

SYSTEM_PROMPT = """You are an expert at extracting relationships that are EXPLICITLY stated in text.

Your task is to:
1. Identify relationships between entities that are directly mentioned in the text
2. Extract the relationship type and supporting evidence
3. Do NOT infer or guess relationships - only extract what is explicitly stated

Rules:
- Every relationship must have direct textual evidence
- Use clear relationship types (founded, works_at, located_in, part_of, etc.)
- Provide the exact text span that states the relationship
- If a relationship is ambiguous or implicit, SKIP it (Stage 3 handles inference)
- Only extract relationships between entities that were identified in Stage 1

Output Format:
Return a JSON array of relationships, each with:
- source_entity_id: ID of source entity
- target_entity_id: ID of target entity
- relationship_type: type of relationship
- evidence: exact text supporting the relationship
"""

USER_PROMPT_TEMPLATE = """Extract all EXPLICIT relationships from the text.

Text:
{text}

Entities:
{entities_list}

Return JSON array of relationships:
[
  {{
    "source_entity_id": "e1",
    "target_entity_id": "e2",
    "relationship_type": "founded|works_at|located_in|etc",
    "evidence": "exact text span from source"
  }}
]

Remember: ONLY extract relationships that are explicitly stated. Do not infer.
"""


def build_relationship_extraction_prompt(text: str, entities: list) -> dict:
    """Build relationship extraction prompt.

    Args:
        text: The original text
        entities: List of Entity objects from Stage 1

    Returns:
        Dictionary with 'system' and 'user' prompts
    """
    # Format entities for prompt
    entities_list = "\n".join([
        f"- {e.id}: {e.text} ({e.type})"
        for e in entities
    ])

    user_prompt = USER_PROMPT_TEMPLATE.format(
        text=text,
        entities_list=entities_list
    )

    return {
        "system": SYSTEM_PROMPT,
        "user": user_prompt
    }
