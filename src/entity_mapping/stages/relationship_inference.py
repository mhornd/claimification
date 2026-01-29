"""Relationship inference stage using LangChain."""

import os
from typing import List
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.prompts import ChatPromptTemplate

from src.entity_mapping.models.entity import Entity
from src.entity_mapping.models.relationship import Relationship
from src.entity_mapping.prompts.relationship_inference import (
    build_relationship_inference_prompt
)


class RelationshipInferenceOutput(BaseModel):
    """Structured output from relationship inference."""
    relationships: List[dict]


class RelationshipInferenceStage:
    """Stage 3: Infer implicit relationships using LLM reasoning."""

    def __init__(
        self,
        model: str = "gpt-5-nano-2025-08-07",
        temperature: float = 0.0,
        confidence_threshold: float = 0.7
    ):
        """Initialize relationship inference stage.

        Args:
            model: LLM model to use
            temperature: Sampling temperature (0.0 for deterministic)
            confidence_threshold: Minimum confidence for inferred relationships
        """
        self.model_name = model
        self.temperature = temperature
        self.confidence_threshold = confidence_threshold
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

    def infer_relationships(
        self,
        text: str,
        entities: List[Entity],
        existing_relationships: List[Relationship]
    ) -> List[Relationship]:
        """Infer implicit relationships from text.

        Args:
            text: The original text
            entities: List of entities from Stage 1
            existing_relationships: Explicit relationships from Stage 2

        Returns:
            List of inferred Relationship objects
        """
        if not entities:
            return []

        # Build prompt
        prompts = build_relationship_inference_prompt(
            text,
            entities,
            existing_relationships
        )

        # Create LangChain prompt template
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", prompts["system"]),
            ("user", prompts["user"])
        ])

        # Create structured output chain
        structured_llm = self.llm.with_structured_output(RelationshipInferenceOutput)
        chain = prompt_template | structured_llm

        # Invoke chain
        result = chain.invoke({})

        # Convert to Relationship objects (all inferred)
        relationships = []
        for rel_dict in result.relationships:
            confidence = rel_dict.get("confidence", 0.0)

            # Filter by confidence threshold
            if confidence < self.confidence_threshold:
                continue

            relationship = Relationship(
                source_entity_id=rel_dict["source_entity_id"],
                target_entity_id=rel_dict["target_entity_id"],
                relationship_type=rel_dict["relationship_type"],
                evidence=rel_dict["evidence"],
                is_inferred=True,  # Stage 3 only produces inferred
                confidence=confidence,
                reasoning=rel_dict["reasoning"]
            )
            relationships.append(relationship)

        return relationships
