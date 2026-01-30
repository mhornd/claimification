"""Test prompts package __init__.py exports."""

import pytest


def test_entity_extraction_exports():
    """Test that entity extraction prompts are exported."""
    from claimification.entity_mapping.prompts import (
        ENTITY_EXTRACTION_SYSTEM_PROMPT,
        ENTITY_EXTRACTION_USER_TEMPLATE,
        build_entity_extraction_prompt
    )

    assert ENTITY_EXTRACTION_SYSTEM_PROMPT is not None
    assert ENTITY_EXTRACTION_USER_TEMPLATE is not None
    assert callable(build_entity_extraction_prompt)


def test_relationship_extraction_exports():
    """Test that relationship extraction prompts are exported."""
    from claimification.entity_mapping.prompts import (
        RELATIONSHIP_EXTRACTION_SYSTEM_PROMPT,
        RELATIONSHIP_EXTRACTION_USER_TEMPLATE,
        build_relationship_extraction_prompt
    )

    assert RELATIONSHIP_EXTRACTION_SYSTEM_PROMPT is not None
    assert RELATIONSHIP_EXTRACTION_USER_TEMPLATE is not None
    assert callable(build_relationship_extraction_prompt)


def test_all_exports_defined():
    """Test that __all__ contains all expected exports."""
    import claimification.entity_mapping.prompts as prompts

    # Check __all__ exists
    assert hasattr(prompts, "__all__")

    # Check all expected items are in __all__
    expected_exports = [
        "ENTITY_EXTRACTION_SYSTEM_PROMPT",
        "ENTITY_EXTRACTION_USER_TEMPLATE",
        "build_entity_extraction_prompt",
        "RELATIONSHIP_EXTRACTION_SYSTEM_PROMPT",
        "RELATIONSHIP_EXTRACTION_USER_TEMPLATE",
        "build_relationship_extraction_prompt"
    ]

    for export in expected_exports:
        assert export in prompts.__all__, f"{export} not in __all__"


def test_imports_work_correctly():
    """Test that all imports resolve to the correct objects."""
    from claimification.entity_mapping.prompts import (
        ENTITY_EXTRACTION_SYSTEM_PROMPT,
        RELATIONSHIP_EXTRACTION_SYSTEM_PROMPT,
        build_entity_extraction_prompt,
        build_relationship_extraction_prompt
    )
    from claimification.entity_mapping.prompts.entity_extraction import (
        SYSTEM_PROMPT as ENTITY_SYSTEM,
    )
    from claimification.entity_mapping.prompts.relationship_extraction import (
        SYSTEM_PROMPT as RELATIONSHIP_SYSTEM,
    )

    # Verify the imports point to the same objects
    assert ENTITY_EXTRACTION_SYSTEM_PROMPT is ENTITY_SYSTEM
    assert RELATIONSHIP_EXTRACTION_SYSTEM_PROMPT is RELATIONSHIP_SYSTEM
