"""Prompts for entity extraction stage."""

SYSTEM_PROMPT = """You are an expert at identifying and extracting named entities from text.

Your task is to:
1. Extract ALL entities mentioned in the text
2. Resolve coreferences (pronouns, abbreviations, aliases to canonical forms)
3. Classify each entity's type accurately
4. Track all mentions of each entity

Rules:
- Use canonical forms (full names, not abbreviations)
  Example: "TechCorp" not "TC", "Sarah Johnson" not "Sarah"
- Classify entity types accurately using these categories:
  PERSON, ORGANIZATION, LOCATION, PRODUCT, EVENT, CONCEPT, DATE, OTHER
- Track all textual mentions of each entity
  Example: "Sarah Johnson" → mentions: ["Sarah", "she", "the founder", "Sarah Johnson"]
- Be conservative - only extract clearly identifiable entities
- Deduplicate: "TechCorp" and "TechCorp GmbH" should be one entity
- For ambiguous cases, use context to disambiguate

Output Format:
Return a JSON array of entities, each with:
- text: canonical name
- type: entity category
- mentions: list of all text spans referring to this entity
"""

USER_PROMPT_TEMPLATE = """Extract all entities from the following text.

Text:
{text}

{context_section}

Return JSON array of entities:
[
  {{
    "text": "canonical entity name",
    "type": "PERSON|ORGANIZATION|LOCATION|PRODUCT|EVENT|CONCEPT|DATE|OTHER",
    "mentions": ["mention1", "mention2", ...]
  }}
]
"""

CONTEXT_SECTION_TEMPLATE = """
Additional Context:
{context}
"""


def build_entity_extraction_prompt(text: str, context: str = None) -> dict:
    """Build entity extraction prompt.

    Args:
        text: The text to extract entities from
        context: Optional additional context

    Returns:
        Dictionary with 'system' and 'user' prompts
    """
    context_section = ""
    if context:
        context_section = CONTEXT_SECTION_TEMPLATE.format(context=context)

    user_prompt = USER_PROMPT_TEMPLATE.format(
        text=text,
        context_section=context_section
    )

    return {
        "system": SYSTEM_PROMPT,
        "user": user_prompt
    }
