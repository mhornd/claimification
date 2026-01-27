# Claimification - Claude Code Plugin Architecture

## Project Overview

Claimification is a Claude Code plugin that extracts and verifies factual claims from question-answer pairs using a multi-stage LangChain-based agent pipeline.

## Directory Structure

```
claimification/
├── .claude-plugin/
│   └── plugin.json                 # Claude Code plugin manifest
│
├── src/
│   ├── __init__.py
│   ├── main.py                     # Main orchestrator
│   ├── pipeline.py                 # Pipeline coordinator
│   │
│   ├── stages/
│   │   ├── __init__.py
│   │   ├── sentence_splitter.py   # Stage 1: Split & Context Creation
│   │   ├── selection_agent.py     # Stage 2: Verifiable Content Detection
│   │   ├── disambiguation_agent.py # Stage 3: Ambiguity Resolution
│   │   └── decomposition_agent.py  # Stage 4: Claim Extraction
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── sentence.py            # Sentence data model
│   │   ├── claim.py               # Claim data model
│   │   └── result.py              # Result aggregation model
│   │
│   ├── prompts/
│   │   ├── __init__.py
│   │   ├── selection.py           # Selection stage prompts
│   │   ├── disambiguation.py      # Disambiguation stage prompts
│   │   └── decomposition.py       # Decomposition stage prompts
│   │
│   └── utils/
│       ├── __init__.py
│       ├── context_builder.py     # Context window builder
│       └── output_formatter.py    # Result formatting
│
├── skills/
│   └── extract-claims              # Claude Code skill
│
├── tests/
│   ├── __init__.py
│   ├── test_pipeline.py
│   ├── test_stages.py
│   └── fixtures/
│       └── sample_qa_pairs.json
│
├── examples/
│   ├── basic_usage.py
│   └── custom_config.py
│
├── docs/
│   ├── INSTALLATION.md
│   ├── USAGE.md
│   ├── API.md
│   └── PRINCIPLES.md              # Core claim extraction principles
│
├── .env.example                    # Environment template
├── .gitignore
├── requirements.txt
├── pyproject.toml                  # Python project config
├── README.md
├── LICENSE
└── CHANGELOG.md
```

## Component Architecture

### Stage Pipeline Flow

```
Input (Q&A Pair)
    ↓
┌─────────────────────────────────────┐
│ Stage 1: Sentence Splitter          │
│ - Split answer into sentences       │
│ - Build context for each sentence   │
│ - Output: List[SentenceWithContext] │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ Stage 2: Selection Agent (LangChain)│
│ - Detect verifiable content         │
│ - Rewrite if partially verifiable   │
│ - Output: SelectionResult           │
└─────────────────────────────────────┘
    ↓ (if has_verifiable_content)
┌─────────────────────────────────────┐
│ Stage 3: Disambiguation Agent       │
│ - Detect ambiguities                │
│ - Resolve using context             │
│ - Output: DisambiguationResult      │
└─────────────────────────────────────┘
    ↓ (if can_be_disambiguated)
┌─────────────────────────────────────┐
│ Stage 4: Decomposition Agent        │
│ - Extract atomic claims             │
│ - Preserve critical context         │
│ - Output: List[Claim]               │
└─────────────────────────────────────┘
    ↓
Aggregated Result
```

## LangChain Integration

### Agent Types

Each stage uses a specialized LangChain agent:

**Selection Agent:**

- Type: `ChatOpenAI` with structured output
- Purpose: Binary classification + rewriting
- Output Schema: `SelectionResult` (has_verifiable_content, rewritten_sentence, reason)

**Disambiguation Agent:**

- Type: `ChatOpenAI` with structured output
- Purpose: Ambiguity detection and resolution
- Output Schema: `DisambiguationResult` (is_ambiguous, can_be_disambiguated, disambiguated_sentence)

**Decomposition Agent:**

- Type: `ChatOpenAI` with structured output
- Purpose: Claim extraction
- Output Schema: `DecompositionResult` (claims: List[str], extraction_reasoning)

### Configuration

```python
# config.py
CLAIMIFICATION_CONFIG = {
    "llm": {
        "model": "gpt-5-nano-2025-08-07",  # or anthropic/claude-3-5-sonnet-20241022
        "temperature": 0.0,  # Deterministic for claim extraction
        "max_tokens": 2000
    },
    "context": {
        "surrounding_sentences": 2,  # Before + after
        "include_headers": True,
        "include_question": True
    },
    "pipeline": {
        "parallel_processing": False,  # Sequential for now
        "max_retries": 3,
        "timeout_seconds": 30
    }
}
```

## Data Models

### Sentence Model

```python
@dataclass
class SentenceWithContext:
    sentence_id: str
    text: str
    context: str
    metadata: Dict[str, Any]  # headers, position, etc.
```

### Result Models

```python
@dataclass
class SelectionResult:
    has_verifiable_content: bool
    rewritten_sentence: Optional[str]
    reason: str

@dataclass
class DisambiguationResult:
    is_ambiguous: bool
    can_be_disambiguated: bool
    disambiguated_sentence: Optional[str]
    ambiguity_explanation: str

@dataclass
class DecompositionResult:
    claims: List[str]
    extraction_reasoning: str

@dataclass
class ClaimExtractionResult:
    source_sentence: str
    status: Literal["extracted", "no_verifiable_claims", "cannot_disambiguate"]
    claims: List[str]
    metadata: Dict[str, Any]
```

## Claude Code Integration

### Plugin Manifest (.claude-plugin/plugin.json)

```json
{
  "name": "claimification",
  "version": "1.0.0",
  "description": "Extract and verify factual claims from LLM outputs",
  "author": "TwoDigits",
  "license": "MIT",
  "repository": "https://github.com/TwoDigits/claimification",
  "skills": ["extract-claims"],
  "requires": {
    "python": ">=3.10",
    "claude-code": ">=1.0.0"
  }
}
```

### Skill Definition (skills/extract-claims)

```yaml
---
name: extract-claims
description: Extract verifiable factual claims from a question-answer pair
---
# Claim Extraction Skill

Use this skill to extract factual claims from LLM-generated answers.
## Usage
```

/extract-claims

```

This will:
1. Ask you for the question and answer
2. Run the 4-stage Claimification pipeline
3. Return structured claims with verification status

## Output Format

For each sentence in the answer:
- **Status:** extracted | no_verifiable_claims | cannot_disambiguate
- **Claims:** List of atomic factual statements
- **Source:** Original sentence with context

## Example

**Input:**
- Question: "What are the challenges in Argentina?"
- Answer: "Argentina's inflation rate reached 25.5% monthly..."

**Output:**
- Claim 1: "Argentina has an inflation rate"
- Claim 2: "Argentina's monthly inflation rate reached 25.5%"
- Source: "Argentina's inflation rate reached 25.5% monthly..."
```

## Implementation Plan

### Phase 1: Core Pipeline (Priority)

1. ✅ Create project structure
2. ⬜ Implement `SentenceSplitter` (Stage 1)
3. ⬜ Implement `SelectionAgent` with LangChain (Stage 2)
4. ⬜ Implement `DisambiguationAgent` with LangChain (Stage 3)
5. ⬜ Implement `DecompositionAgent` with LangChain (Stage 4)
6. ⬜ Create `Pipeline` orchestrator

### Phase 2: Claude Code Integration

7. ⬜ Create plugin manifest
8. ⬜ Implement `extract-claims` skill
9. ⬜ Add CLI interface

### Phase 3: Testing & Documentation

10. ⬜ Write unit tests for each stage
11. ⬜ Create integration tests
12. ⬜ Write comprehensive README
13. ⬜ Create usage examples

### Phase 4: Marketplace Preparation

14. ⬜ Add metadata for TwoDigits Marketplace
15. ⬜ Security review
16. ⬜ Performance optimization

## Technical Decisions

### Why LangChain?

- **Structured Output:** Native support for JSON schema validation
- **Agent Abstraction:** Clean separation of prompt + model + parser
- **Retry Logic:** Built-in error handling
- **Model Agnostic:** Easy to switch between OpenAI/Anthropic/etc.

### Why NOT MCP Server?

- **Direct Integration:** Runs as native Python code in Claude Code
- **Simpler Deployment:** No server process to manage
- **Lower Latency:** Direct function calls
- **Better Control:** Full pipeline visibility

### Why Python?

- **LangChain Native:** Best LangChain support
- **Rich NLP Tools:** spaCy, NLTK for sentence splitting
- **Type Safety:** Pydantic models for structured output
- **Claude Code Support:** First-class Python skill support

## Dependencies

```txt
# Core
langchain>=0.1.0
langchain-openai>=0.0.5  # or langchain-anthropic
pydantic>=2.0.0

# NLP
spacy>=3.7.0
en_core_web_sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.0/en_core_web_sm-3.7.0-py3-none-any.whl

# Utilities
python-dotenv>=1.0.0
rich>=13.0.0  # For beautiful CLI output

# Testing
pytest>=7.4.0
pytest-asyncio>=0.21.0
```

## Environment Variables

```bash
# .env.example
OPENAI_API_KEY=sk-...
# OR
ANTHROPIC_API_KEY=sk-ant-...

# Model configuration
CLAIMIFICATION_MODEL=gpt-5-nano-2025-08-07
CLAIMIFICATION_TEMPERATURE=0.0

# Context configuration
CLAIMIFICATION_CONTEXT_SENTENCES=2
```

## Usage Example

```python
from claimification import ClaimificationPipeline

# Initialize pipeline
pipeline = ClaimificationPipeline(
    model="gpt-5-nano-2025-08-07",
    temperature=0.0
)

# Extract claims
result = pipeline.extract_claims(
    question="What are challenges in Argentina?",
    answer="Argentina's inflation rate reached 25.5% monthly..."
)

# Access results
for sentence_result in result.sentences:
    print(f"Sentence: {sentence_result.source_sentence}")
    print(f"Status: {sentence_result.status}")
    for claim in sentence_result.claims:
        print(f"  - {claim}")
```

## Next Steps

1. Start with Stage 1 (Sentence Splitter) - no LLM needed
2. Implement Stage 2 (Selection Agent) with structured output
3. Test with examples from explanation.md
4. Iterate on prompt engineering for accuracy
5. Add remaining stages
6. Integrate with Claude Code skills

## References

- Paper: "Towards Effective Extraction and Evaluation of Factual Claims"
- Original flow: `flow.txt`
- Explanation: `explanation.md`
- Marketplace standards: `README_of_marketplace_claude_code.md`
