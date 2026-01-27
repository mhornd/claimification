"""Stage 4: Decomposition Agent - Claim Extraction.

This agent decomposes sentences into atomic, standalone factual claims.
"""

from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.prompts import ChatPromptTemplate

from ..models import DecompositionResult, StageResult
from ..prompts.decomposition import (
    DECOMPOSITION_SYSTEM_PROMPT,
    create_decomposition_prompt
)


class DecompositionAgent:
    """Agent for extracting atomic claims from sentences."""

    def __init__(
        self,
        model: str = "gpt-4o",
        temperature: float = 0.0,
        max_tokens: int = 2000,
        max_retries: int = 3
    ):
        """Initialize the Decomposition Agent.

        Args:
            model: LLM model to use (e.g., "gpt-4o", "claude-3-5-sonnet-20241022")
            temperature: Temperature for LLM (0.0 for deterministic)
            max_tokens: Maximum tokens for response
            max_retries: Maximum number of retries on failure
        """
        self.model_name = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.max_retries = max_retries

        # Initialize LLM based on model name
        if "gpt" in model or "openai" in model:
            self.llm = ChatOpenAI(
                model=model,
                temperature=temperature,
                max_tokens=max_tokens
            )
        elif "claude" in model or "anthropic" in model:
            self.llm = ChatAnthropic(
                model=model,
                temperature=temperature,
                max_tokens=max_tokens
            )
        else:
            raise ValueError(f"Unsupported model: {model}")

        # Create structured output LLM
        self.structured_llm = self.llm.with_structured_output(
            DecompositionResult)

        # Create prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", DECOMPOSITION_SYSTEM_PROMPT),
            ("user", "{user_prompt}")
        ])

    def process(self, sentence: str, context: str) -> StageResult:
        """Process a sentence to extract atomic claims.

        Args:
            sentence: The sentence to decompose
            context: Context surrounding the sentence

        Returns:
            StageResult containing DecompositionResult or error
        """
        try:
            # Create user prompt
            user_prompt = create_decomposition_prompt(sentence, context)

            # Create chain
            chain = self.prompt | self.structured_llm

            # Execute with retries
            for attempt in range(self.max_retries):
                try:
                    result = chain.invoke({
                        "user_prompt": user_prompt
                    })
                    # Convert dict to DecompositionResult if needed
                    if isinstance(result, dict):
                        result = DecompositionResult(**result)
                    return StageResult(success=True, data=result)
                except Exception as e:
                    if attempt == self.max_retries - 1:
                        raise
                    continue

        except Exception as e:
            return StageResult(
                success=False,
                error=f"Decomposition failed: {str(e)}"
            )

    def process_batch(self, sentences_with_context: list[tuple[str, str]]) -> list[StageResult]:
        """Process multiple sentences in batch.

        Args:
            sentences_with_context: List of (sentence, context) tuples

        Returns:
            List of StageResult objects
        """
        results = []
        for sentence, context in sentences_with_context:
            result = self.process(sentence, context)
            results.append(result)
        return results
