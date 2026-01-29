"""Entity extraction stage using LangChain."""

import os
from typing import List, Optional
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.prompts import ChatPromptTemplate

from src.entity_mapping.models.entity import Entity, EntityType
from src.entity_mapping.prompts.entity_extraction import build_entity_extraction_prompt


class EntityExtractionOutput(BaseModel):
    """Structured output from entity extraction."""
    entities: List[dict]


class EntityExtractionStage:
    """Stage 1: Extract entities from text with coreference resolution."""

    def __init__(
        self,
        model: str = "gpt-5-nano-2025-08-07",
        temperature: float = 0.0
    ):
        """Initialize entity extraction stage.

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

    def extract_entities(
        self,
        text: str,
        context: Optional[str] = None
    ) -> List[Entity]:
        """Extract entities from text.

        Args:
            text: The text to extract entities from
            context: Optional contextual information

        Returns:
            List of extracted Entity objects
        """
        # Build prompt
        prompts = build_entity_extraction_prompt(text, context)

        # Create LangChain prompt template
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", prompts["system"]),
            ("user", prompts["user"])
        ])

        # Create structured output chain
        structured_llm = self.llm.with_structured_output(EntityExtractionOutput)
        chain = prompt_template | structured_llm

        # Invoke chain
        result = chain.invoke({})

        # Convert to Entity objects with IDs
        entities = []
        for i, entity_dict in enumerate(result.entities, start=1):
            entity = Entity(
                id=f"e{i}",
                text=entity_dict["text"],
                type=EntityType(entity_dict["type"]),
                mentions=entity_dict.get("mentions", [entity_dict["text"]]),
                context=context
            )
            entities.append(entity)

        return entities
