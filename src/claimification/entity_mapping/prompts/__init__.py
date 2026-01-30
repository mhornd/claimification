"""Prompts for entity relationship mapping stages."""

from claimification.entity_mapping.prompts.entity_extraction import (
    SYSTEM_PROMPT as ENTITY_EXTRACTION_SYSTEM_PROMPT,
    USER_PROMPT_TEMPLATE as ENTITY_EXTRACTION_USER_TEMPLATE,
    build_entity_extraction_prompt
)
from claimification.entity_mapping.prompts.relationship_extraction import (
    SYSTEM_PROMPT as RELATIONSHIP_EXTRACTION_SYSTEM_PROMPT,
    USER_PROMPT_TEMPLATE as RELATIONSHIP_EXTRACTION_USER_TEMPLATE,
    build_relationship_extraction_prompt
)
from claimification.entity_mapping.prompts.relationship_inference import (
    SYSTEM_PROMPT as RELATIONSHIP_INFERENCE_SYSTEM_PROMPT,
    USER_PROMPT_TEMPLATE as RELATIONSHIP_INFERENCE_USER_TEMPLATE,
    build_relationship_inference_prompt
)

__all__ = [
    "ENTITY_EXTRACTION_SYSTEM_PROMPT",
    "ENTITY_EXTRACTION_USER_TEMPLATE",
    "build_entity_extraction_prompt",
    "RELATIONSHIP_EXTRACTION_SYSTEM_PROMPT",
    "RELATIONSHIP_EXTRACTION_USER_TEMPLATE",
    "build_relationship_extraction_prompt",
    "RELATIONSHIP_INFERENCE_SYSTEM_PROMPT",
    "RELATIONSHIP_INFERENCE_USER_TEMPLATE",
    "build_relationship_inference_prompt"
]
