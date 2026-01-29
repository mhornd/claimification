"""Explicit relationship extraction stage using LangChain."""

import os
from typing import List
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.prompts import ChatPromptTemplate

from src.entity_mapping.models.entity import Entity
from src.entity_mapping.models.relationship import Relationship
from src.entity_mapping.prompts.relationship_extraction import (
    build_relationship_extraction_prompt
)


class RelationshipExtractionOutput(BaseModel):
    """Structured output from relationship extraction."""
    relationships: List[dict]


class RelationshipExtractionStage:
    """Stage 2: Extract explicit relationships from text."""

    def __init__(
        self,
        model: str = "gpt-5-nano-2025-08-07",
        temperature: float = 0.0
    ):
        """Initialize relationship extraction stage.

        Args:
            model: LLM model to use
            temperature: Sampling temperature (0.0 for deterministic)
        """
        self.model_name = model
        self.temperature = temperature
        self.llm = self._initialize_llm()

    def _initialize_llm(self):
        """Initialize LangChain LLM client."""
        if "gpt" in self.model_name or "o1" in self.model_name:
            return ChatOpenAI(
                model=self.model_name,
                temperature=self.temperature,
                api_key=os.getenv("OPENAI_API_KEY")
            )
        elif "claude" in self.model_name:
            return ChatAnthropic(
                model=self.model_name,
                temperature=self.temperature,
                api_key=os.getenv("ANTHROPIC_API_KEY")
            )
        else:
            raise ValueError(f"Unsupported model: {self.model_name}")

    def extract_relationships(
        self,
        text: str,
        entities: List[Entity]
    ) -> List[Relationship]:
        """Extract explicit relationships from text.

        Args:
            text: The original text
            entities: List of entities from Stage 1

        Returns:
            List of explicit Relationship objects
        """
        if not entities:
            return []

        # Build prompt
        prompts = build_relationship_extraction_prompt(text, entities)

        # Create LangChain prompt template
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", prompts["system"]),
            ("user", prompts["user"])
        ])

        # Create structured output chain
        structured_llm = self.llm.with_structured_output(RelationshipExtractionOutput)
        chain = prompt_template | structured_llm

        # Invoke chain
        result = chain.invoke({})

        # Convert to Relationship objects (all explicit)
        relationships = []
        for rel_dict in result.relationships:
            relationship = Relationship(
                source_entity_id=rel_dict["source_entity_id"],
                target_entity_id=rel_dict["target_entity_id"],
                relationship_type=rel_dict["relationship_type"],
                evidence=rel_dict["evidence"],
                is_inferred=False,  # Stage 2 only extracts explicit
                confidence=1.0      # Explicit relationships always 1.0
            )
            relationships.append(relationship)

        return relationships
