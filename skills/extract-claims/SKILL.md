---
name: extract-claims
description: Extract verifiable factual claims from a question-answer pair using the Claimification pipeline
---

# Extract Claims Skill

Use this skill to extract factual claims from LLM-generated answers using the Claimification multi-stage pipeline.

## What This Does

Claimification processes question-answer pairs through four stages:

1. **Sentence Splitting:** Breaks the answer into sentences with context
2. **Selection:** Identifies sentences with verifiable content
3. **Disambiguation:** Resolves ambiguous references using context
4. **Decomposition:** Extracts atomic, standalone factual claims

## When to Use

Use this skill when you need to:

- Verify LLM outputs for factual accuracy
- Extract structured claims for fact-checking
- Identify which parts of an answer are verifiable
- Break down complex answers into atomic statements

## Usage

```
/extract-claims
```

Claude will ask you for:

1. The **question** that prompted the answer
2. The **answer** text to analyze

## Example

**Input:**

- Question: "What are the economic challenges in Argentina?"
- Answer: "Argentina's rampant inflation, with monthly rates reaching as high as 25.5%, has made many goods unobtainable and plunged the value of the currency, causing severe economic hardship."

**Output:**

```
A. Argentina's rampant inflation, with monthly rates reaching as high as 25.5%, has made many goods unobtainable and plunged the value of the currency, causing severe economic hardship.

1. Argentina has rampant inflation.
2. Argentina's monthly inflation rates have reached as high as 25.5%.
3. Inflation has made many goods unobtainable in Argentina.
4. Inflation has plunged the value of Argentina's currency.
5. Inflation has caused severe economic hardship in Argentina.
```

## Output Format

For each sentence in the answer:

- **Source Sentence:** The original sentence
- **Status:**
  - ✅ `extracted` - Claims successfully extracted
  - ❌ `no_verifiable_claims` - No verifiable content found
  - ⚠️ `cannot_disambiguate` - Ambiguity cannot be resolved
  - 🔴 `processing_error` - Processing failed
- **Claims:** List of atomic factual statements (if status is `extracted`)

## Configuration

Set these environment variables to customize behavior:

```bash
# API Key (required - choose one)
OPENAI_API_KEY=sk-...
# or
ANTHROPIC_API_KEY=sk-ant-...

# Model selection
CLAIMIFICATION_MODEL=gpt-5-nano-2025-08-07  # or claude-3-5-sonnet-20241022

# Context window
CLAIMIFICATION_CONTEXT_SENTENCES=2  # sentences before/after for context
```

## Core Principles

Claimification follows these principles:

1. **Capture all verifiable content** - Nothing verifiable is omitted
2. **Exclude unverifiable content** - Opinions and recommendations are filtered
3. **Claims are entailed** - Each claim is fully supported by the source
4. **Claims are standalone** - Understandable without additional context
5. **Preserve critical context** - Context affecting meaning is included
6. **Flag unresolvable ambiguity** - Ambiguous sentences are marked, not guessed

## Limitations

- Requires OpenAI or Anthropic API access
- Processing time depends on answer length
- Best suited for factual, informative answers (not creative or conversational text)
- May require manual review for domain-specific terminology

## Technical Details

**Pipeline Architecture:**

- Built with LangChain for agent orchestration
- Uses structured output for reliable parsing
- Temperature set to 0.0 for deterministic results
- Automatic retry logic for API failures

**Models Supported:**

- OpenAI: GPT-4, GPT-5-nano, GPT-3.5-turbo
- Anthropic: Claude 3.5 Sonnet, Claude 3 Opus

## Related

- Based on the research paper: "Towards Effective Extraction and Evaluation of Factual Claims"
- Designed for integration with fact-checking systems like Azure AI Groundedness Detection
- Compatible with enterprise verification workflows

## Support

- GitHub: https://github.com/TwoDigits/claimification
- Issues: https://github.com/TwoDigits/claimification/issues
- Documentation: https://github.com/TwoDigits/claimification/tree/main/docs
