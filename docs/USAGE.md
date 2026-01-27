# Usage Guide

This guide covers different ways to use Claimification.

## Table of Contents

- [Claude Code Skill](#claude-code-skill)
- [Command Line Interface](#command-line-interface)
- [Python API](#python-api)
- [Configuration](#configuration)

## Claude Code Skill

The simplest way to use Claimification is through the Claude Code skill.

### Basic Usage

```bash
/extract-claims
```

Claude will prompt you for:

1. The question that prompted the answer
2. The answer text to analyze

### Example Session

```
You: /extract-claims

Claude: I'll extract factual claims from a question-answer pair.

What is the question that prompted this answer?

You: What are the economic challenges in Argentina?

Claude: Now, please provide the answer text to analyze.

You: Argentina's rampant inflation, with monthly rates reaching
as high as 25.5%, has made many goods unobtainable and plunged
the value of the currency, causing severe economic hardship.

Claude: [Processes through 4-stage pipeline]

Results:
A. Argentina's rampant inflation, with monthly rates reaching as
high as 25.5%, has made many goods unobtainable and plunged the
value of the currency, causing severe economic hardship.

1. Argentina has rampant inflation.
2. Argentina's monthly inflation rates have reached as high as 25.5%.
3. Inflation has made many goods unobtainable in Argentina.
4. Inflation has plunged the value of Argentina's currency.
5. Inflation has caused severe economic hardship in Argentina.
```

## Command Line Interface

Use the CLI for batch processing or integration with scripts.

### Basic Command

```bash
python -m src.main \
    --question "Your question here" \
    --answer "Your answer here"
```

### Using an Answer File

```bash
python -m src.main \
    --question "What are challenges in Argentina?" \
    --answer-file answer.txt
```

### Output to File

```bash
python -m src.main \
    --question "Your question" \
    --answer "Your answer" \
    --output results.md \
    --format markdown
```

### JSON Output

```bash
python -m src.main \
    --question "Your question" \
    --answer "Your answer" \
    --format json \
    --output results.json
```

### Custom Model

```bash
python -m src.main \
    --question "Your question" \
    --answer "Your answer" \
    --model claude-3-5-sonnet-20241022
```

### Quiet Mode

```bash
python -m src.main \
    --question "Your question" \
    --answer "Your answer" \
    --quiet
```

## Python API

Use the Python API for programmatic integration.

### Basic Example

```python
from src import ClaimificationPipeline

# Initialize pipeline
pipeline = ClaimificationPipeline(
    model="gpt-5-nano-2025-08-07",
    temperature=0.0,
    context_sentences=2,
    verbose=True
)

# Extract claims
result = pipeline.extract_claims(
    question="What are economic challenges in Argentina?",
    answer="Argentina's inflation rate reached 25.5%..."
)

# Process results
for sentence_result in result.sentence_results:
    print(f"Sentence: {sentence_result.source_sentence}")
    print(f"Status: {sentence_result.status}")

    if sentence_result.claims:
        for claim in sentence_result.claims:
            print(f"  - {claim.text}")
```

### Access Statistics

```python
# Get summary statistics
stats = result.get_statistics_summary()
print(f"Total claims: {stats['total_claims']}")
print(f"Success rate: {stats['extracted']}/{stats['total_sentences']}")
```

### Get All Claims

```python
# Get list of all successfully extracted claims
all_claims = result.get_all_claims()

for claim in all_claims:
    print(f"[{claim.source_sentence_id}] {claim.text}")
```

### Filter by Status

```python
from src import SentenceStatus

# Get only successfully extracted sentences
successful = [
    r for r in result.sentence_results
    if r.status == SentenceStatus.EXTRACTED
]

# Get sentences that couldn't be disambiguated
ambiguous = [
    r for r in result.sentence_results
    if r.status == SentenceStatus.CANNOT_DISAMBIGUATE
]
```

### Custom Configuration

```python
from src import ClaimificationPipeline

pipeline = ClaimificationPipeline(
    model="claude-3-5-sonnet-20241022",  # Use Claude instead of GPT
    temperature=0.1,                      # Slightly less deterministic
    context_sentences=3,                  # More context
    verbose=False                         # No progress output
)
```

## Configuration

### Environment Variables

Set these in your `.env` file or shell:

```bash
# API Keys (required)
OPENAI_API_KEY=sk-proj-...
# OR
ANTHROPIC_API_KEY=sk-ant-...

# Model Configuration (optional)
CLAIMIFICATION_MODEL=gpt-5-nano-2025-08-07
CLAIMIFICATION_TEMPERATURE=0.0
CLAIMIFICATION_MAX_TOKENS=2000

# Context Configuration (optional)
CLAIMIFICATION_CONTEXT_SENTENCES=2
CLAIMIFICATION_INCLUDE_HEADERS=true
CLAIMIFICATION_INCLUDE_QUESTION=true

# Pipeline Configuration (optional)
CLAIMIFICATION_MAX_RETRIES=3
CLAIMIFICATION_TIMEOUT_SECONDS=30
```

### Model Selection

**OpenAI Models:**

- `gpt-5-nano-2025-08-07` (recommended) - Best balance of quality and speed
- `gpt-4` - Highest quality, slower
- `gpt-3.5-turbo` - Faster, lower cost, slightly lower quality

**Anthropic Models:**

- `claude-3-5-sonnet-20241022` (recommended) - Best overall
- `claude-3-opus-20240229` - Highest quality

### Context Window Size

`context_sentences` controls how many surrounding sentences are included:

- `0`: No context (not recommended)
- `1`: Immediately adjacent sentences
- `2`: Standard (recommended)
- `3+`: Extended context (may increase costs)

### Temperature

- `0.0`: Fully deterministic (recommended for consistency)
- `0.1-0.3`: Slightly more creative
- `0.5+`: Not recommended (reduces reliability)

## Output Formats

### Markdown Format

Human-readable format with headers and bullet points:

```markdown
## Extracted Claims

A. Argentina's inflation rate reached 25.5%.

1. Argentina has an inflation rate.
2. Argentina's inflation rate reached 25.5%.
```

### JSON Format

Machine-readable format for integration:

```json
{
  "question": "What are challenges in Argentina?",
  "answer": "Argentina's inflation rate reached 25.5%.",
  "statistics": {
    "total_sentences": 1,
    "total_claims": 2,
    "extracted": 1
  },
  "sentences": [
    {
      "sentence_id": "sent_000",
      "source_sentence": "Argentina's inflation rate reached 25.5%.",
      "status": "extracted",
      "claims": [
        "Argentina has an inflation rate.",
        "Argentina's inflation rate reached 25.5%."
      ]
    }
  ]
}
```

## Best Practices

### 1. Provide Good Questions

The question provides important context. Be specific:

✅ Good: "What are the economic challenges facing Argentina in 2024?"
❌ Poor: "Tell me about Argentina"

### 2. Use Appropriate Models

- **gpt-5-nano-2025-08-07**: Best default choice
- **claude-3-5-sonnet**: Alternative with different strengths
- **gpt-3.5-turbo**: Only for cost-sensitive applications

### 3. Set Temperature to 0.0

For fact extraction, consistency is more important than creativity.

### 4. Review Ambiguous Sentences

Sentences marked as "cannot_disambiguate" may need manual review:

```python
ambiguous = [
    r for r in result.sentence_results
    if r.status == SentenceStatus.CANNOT_DISAMBIGUATE
]

for sentence in ambiguous:
    print(f"Needs review: {sentence.source_sentence}")
    print(f"Reason: {sentence.metadata['ambiguity_explanation']}")
```

### 5. Batch Processing

For multiple Q&A pairs, reuse the pipeline instance:

```python
from src import ClaimificationPipeline

pipeline = ClaimificationPipeline()

for qa_pair in qa_pairs:
    result = pipeline.extract_claims(
        question=qa_pair['question'],
        answer=qa_pair['answer']
    )
    # Process result...
```

## Troubleshooting

### Slow Processing

- Use `gpt-5-nano-2025-08-07` instead of `gpt-4`
- Reduce `context_sentences`
- Consider parallel processing for multiple Q&A pairs

### High API Costs

- Use `gpt-3.5-turbo` instead of `gpt-5-nano-2025-08-07`
- Reduce answer length before processing
- Batch similar questions

### Poor Quality Claims

- Increase `context_sentences`
- Use `gpt-5-nano-2025-08-07` or `claude-3-5-sonnet`
- Provide more specific questions
- Review the source answer quality

## Next Steps

- See [API.md](API.md) for detailed API reference
- Check [examples/](../examples/) for more code examples
- Read [PRINCIPLES.md](PRINCIPLES.md) to understand the methodology
