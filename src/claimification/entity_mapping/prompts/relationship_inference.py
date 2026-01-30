"""Prompts for relationship inference stage."""

SYSTEM_PROMPT = """You are an expert at inferring implicit relationships using logical reasoning.

Your task is to:
1. Identify entity pairs that co-occur but lack explicit relationships
2. Infer logical relationships based on context and common sense
3. Provide confidence scores and reasoning for each inference

Rules:
- Only infer relationships with high confidence (>0.7)
- Always provide clear reasoning/justification
- Conservative approach: when uncertain, don't infer
- Consider context and common-sense knowledge
- Examples of valid inferences:
  * "hired as CTO" → infers "works_at" (confidence: 0.95)
  * "CEO of X" + "X based in Berlin" → infers "located_in" (confidence: 0.90)

Output Format:
Return a JSON array of inferred relationships, each with:
- source_entity_id: ID of source entity
- target_entity_id: ID of target entity
- relationship_type: inferred relationship type
- evidence: text that supports the inference
- confidence: score between 0.7 and 1.0
- reasoning: explanation of why this relationship was inferred
"""

USER_PROMPT_TEMPLATE = """Infer implicit relationships from the text.

Text:
{text}

Entities:
{entities_list}

Existing Explicit Relationships:
{existing_relationships}

Identify entity pairs that co-occur but have no explicit relationship, and infer logical connections.

Return JSON array of inferred relationships:
[
  {{
    "source_entity_id": "e1",
    "target_entity_id": "e2",
    "relationship_type": "inferred_type",
    "evidence": "text supporting inference",
    "confidence": 0.85,
    "reasoning": "explanation of inference"
  }}
]

Only include inferences with confidence > 0.7. Be conservative.
"""


def build_relationship_inference_prompt(
    text: str,
    entities: list,
    existing_relationships: list
) -> dict:
    """Build relationship inference prompt.

    Args:
        text: The original text
        entities: List of Entity objects
        existing_relationships: List of Relationship objects from Stage 2

    Returns:
        Dictionary with 'system' and 'user' prompts
    """
    # Format entities for prompt
    entities_list = "\n".join([
        f"- {e.id}: {e.text} ({e.type})"
        for e in entities
    ])

    # Format existing relationships
    if existing_relationships:
        rel_lines = [
            f"- {r.source_entity_id} → {r.target_entity_id}: {r.relationship_type}"
            for r in existing_relationships
        ]
        existing_rels_str = "\n".join(rel_lines)
    else:
        existing_rels_str = "(none)"

    user_prompt = USER_PROMPT_TEMPLATE.format(
        text=text,
        entities_list=entities_list,
        existing_relationships=existing_rels_str
    )

    return {
        "system": SYSTEM_PROMPT,
        "user": user_prompt
    }
