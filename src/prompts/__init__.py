"""Prompts for LLM agents."""

from .selection import (
    SELECTION_SYSTEM_PROMPT,
    SELECTION_USER_PROMPT_TEMPLATE,
    create_selection_prompt
)
from .disambiguation import (
    DISAMBIGUATION_SYSTEM_PROMPT,
    DISAMBIGUATION_USER_PROMPT_TEMPLATE,
    create_disambiguation_prompt
)
from .decomposition import (
    DECOMPOSITION_SYSTEM_PROMPT,
    DECOMPOSITION_USER_PROMPT_TEMPLATE,
    create_decomposition_prompt
)

__all__ = [
    # Selection prompts
    "SELECTION_SYSTEM_PROMPT",
    "SELECTION_USER_PROMPT_TEMPLATE",
    "create_selection_prompt",
    # Disambiguation prompts
    "DISAMBIGUATION_SYSTEM_PROMPT",
    "DISAMBIGUATION_USER_PROMPT_TEMPLATE",
    "create_disambiguation_prompt",
    # Decomposition prompts
    "DECOMPOSITION_SYSTEM_PROMPT",
    "DECOMPOSITION_USER_PROMPT_TEMPLATE",
    "create_decomposition_prompt",
]
