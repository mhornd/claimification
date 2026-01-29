"""Test relationship extraction prompts."""

import pytest
from src.entity_mapping.models.entity import Entity, EntityType
from src.entity_mapping.prompts.relationship_extraction import (
    SYSTEM_PROMPT,
    USER_PROMPT_TEMPLATE,
    build_relationship_extraction_prompt
)


def test_system_prompt_exists():
    """Test that SYSTEM_PROMPT constant exists."""
    assert SYSTEM_PROMPT is not None
    assert isinstance(SYSTEM_PROMPT, str)
    assert len(SYSTEM_PROMPT) > 0


def test_system_prompt_emphasizes_explicit_relationships():
    """Test that system prompt emphasizes EXPLICIT relationships only."""
    assert "EXPLICIT" in SYSTEM_PROMPT.upper()
    assert "NOT INFER" in SYSTEM_PROMPT.upper() or "DO NOT INFER" in SYSTEM_PROMPT.upper()


def test_system_prompt_mentions_stage_3_inference():
    """Test that system prompt mentions Stage 3 handles inference."""
    # Should guide away from inference by mentioning it's handled later
    assert "STAGE 3" in SYSTEM_PROMPT.upper() or "INFERENCE" in SYSTEM_PROMPT.upper()


def test_system_prompt_specifies_output_format():
    """Test that system prompt specifies JSON output format."""
    assert "json" in SYSTEM_PROMPT.lower()
    assert "source_entity_id" in SYSTEM_PROMPT
    assert "target_entity_id" in SYSTEM_PROMPT
    assert "relationship_type" in SYSTEM_PROMPT
    assert "evidence" in SYSTEM_PROMPT


def test_user_prompt_template_exists():
    """Test that USER_PROMPT_TEMPLATE constant exists."""
    assert USER_PROMPT_TEMPLATE is not None
    assert isinstance(USER_PROMPT_TEMPLATE, str)
    assert len(USER_PROMPT_TEMPLATE) > 0


def test_user_prompt_template_has_placeholders():
    """Test that user prompt template has required placeholders."""
    assert "{text}" in USER_PROMPT_TEMPLATE
    assert "{entities_list}" in USER_PROMPT_TEMPLATE


def test_build_relationship_extraction_prompt_with_entities():
    """Test building relationship extraction prompt with entities."""
    # Create sample entities
    entities = [
        Entity(
            id="e1",
            text="TechCorp",
            type=EntityType.ORGANIZATION,
            mentions=["TechCorp", "the company"]
        ),
        Entity(
            id="e2",
            text="Sarah Johnson",
            type=EntityType.PERSON,
            mentions=["Sarah Johnson", "Sarah", "she"]
        )
    ]

    text = "Sarah Johnson founded TechCorp in 2020."

    result = build_relationship_extraction_prompt(text, entities)

    # Should return dict with system and user prompts
    assert isinstance(result, dict)
    assert "system" in result
    assert "user" in result


def test_build_prompt_returns_system_prompt():
    """Test that build function returns the SYSTEM_PROMPT."""
    entities = [
        Entity(id="e1", text="Test", type=EntityType.PERSON, mentions=["Test"])
    ]

    result = build_relationship_extraction_prompt("Test text", entities)

    assert result["system"] == SYSTEM_PROMPT


def test_build_prompt_includes_text_in_user_prompt():
    """Test that build function includes text in user prompt."""
    entities = [
        Entity(id="e1", text="Test", type=EntityType.PERSON, mentions=["Test"])
    ]
    text = "This is the test text to analyze."

    result = build_relationship_extraction_prompt(text, entities)

    assert text in result["user"]


def test_build_prompt_includes_entities_list():
    """Test that build function includes formatted entities list."""
    entities = [
        Entity(
            id="e1",
            text="TechCorp",
            type=EntityType.ORGANIZATION,
            mentions=["TechCorp"]
        ),
        Entity(
            id="e2",
            text="Sarah Johnson",
            type=EntityType.PERSON,
            mentions=["Sarah"]
        )
    ]

    result = build_relationship_extraction_prompt("Some text", entities)

    # Should contain entity IDs, text, and types
    assert "e1" in result["user"]
    assert "TechCorp" in result["user"]
    assert "ORGANIZATION" in result["user"]
    assert "e2" in result["user"]
    assert "Sarah Johnson" in result["user"]
    assert "PERSON" in result["user"]


def test_build_prompt_with_empty_entities():
    """Test building prompt with empty entities list."""
    result = build_relationship_extraction_prompt("Test text", [])

    # Should still return valid structure
    assert isinstance(result, dict)
    assert "system" in result
    assert "user" in result
    assert "Test text" in result["user"]


def test_user_prompt_emphasizes_explicit_only():
    """Test that user prompt template reminds about explicit relationships."""
    # Template should remind user to only extract explicit relationships
    assert "EXPLICIT" in USER_PROMPT_TEMPLATE.upper() or "explicit" in USER_PROMPT_TEMPLATE.lower()
