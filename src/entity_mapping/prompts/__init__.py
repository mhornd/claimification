"""Prompts for entity relationship mapping stages."""

from src.entity_mapping.prompts.entity_extraction import (
    SYSTEM_PROMPT as ENTITY_EXTRACTION_SYSTEM_PROMPT,
    USER_PROMPT_TEMPLATE as ENTITY_EXTRACTION_USER_TEMPLATE,
    build_entity_extraction_prompt
)

__all__ = [
    "ENTITY_EXTRACTION_SYSTEM_PROMPT",
    "ENTITY_EXTRACTION_USER_TEMPLATE",
    "build_entity_extraction_prompt"
]
