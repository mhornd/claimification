"""Stage 2: Selection Agent - Verifiable Content Detection.

This agent determines if a sentence contains verifiable content
and rewrites it if it contains both verifiable and unverifiable parts.
"""

from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate

from ..models import SelectionResult, StageResult
from ..prompts.selection import (
    SELECTION_SYSTEM_PROMPT,
    create_selection_prompt
)


class SelectionAgent:
    """Agent for detecting verifiable content in sentences."""

    def __init__(
        self,
        model: str = "gpt-5-nano-2025-08-07",
        temperature: float = 0.0,
        max_tokens: int = 1000,
        max_retries: int = 3
    ):
        """Initialize the Selection Agent.

        Args:
            model: LLM model to use (e.g., "gpt-5-nano-2025-08-07", "claude-3-5-sonnet-20241022")
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
            # Use max_completion_tokens for newer models (gpt-5-nano, gpt-4o, etc.)
            # For reasoning models, set reasoning_effort to "low" to minimize token usage
            if "gpt-5" in model or "gpt-4o" in model:
                model_kwargs = {
                    "max_completion_tokens": max_tokens,
                }
                # Add reasoning_effort for reasoning models
                if "gpt-5" in model or "o1" in model:
                    model_kwargs["reasoning_effort"] = "low"

                self.llm = ChatOpenAI(
                    model=model,
                    temperature=temperature,
                    model_kwargs=model_kwargs
                )
            else:
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
        self.structured_llm = self.llm.with_structured_output(SelectionResult)

        # Create prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", SELECTION_SYSTEM_PROMPT),
            ("user", "{user_prompt}")
        ])

    def process(self, sentence: str, context: str) -> StageResult:
        """Process a sentence to detect verifiable content.

        Args:
            sentence: The sentence to analyze
            context: Context surrounding the sentence

        Returns:
            StageResult containing SelectionResult or error
        """
        try:
            # Create user prompt
            user_prompt = create_selection_prompt(sentence, context)

            # Create chain
            chain = self.prompt | self.structured_llm

            # Execute with retries
            for attempt in range(self.max_retries):
                try:
                    result = chain.invoke({
                        "user_prompt": user_prompt
                    })
                    # Convert dict to SelectionResult if needed
                    if isinstance(result, dict):
                        result = SelectionResult(**result)
                    return StageResult(success=True, data=result)
                except Exception as e:
                    if attempt == self.max_retries - 1:
                        raise
                    continue

        except Exception as e:
            return StageResult(
                success=False,
                error=f"Selection failed: {str(e)}"
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
