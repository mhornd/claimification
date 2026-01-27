# Claimification

> **Extract verifiable factual claims from LLM-generated answers using a multi-stage AI pipeline**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/LangChain-Enabled-green.svg)](https://langchain.com/)

Claimification is a Claude Code plugin that implements a sophisticated claim extraction pipeline based on the research paper **"Towards Effective Extraction and Evaluation of Factual Claims"** by Metropolitansky & Larson (2025). It breaks down LLM-generated text into atomic, verifiable factual statements that can be independently fact-checked.

## Why Claimification?

Large language models can produce impressive outputs, but they sometimes include inaccuracies or unsubstantiated claims. Claimification helps by:

✅ **Extracting verifiable facts** from complex LLM outputs
✅ **Filtering out opinions** and non-verifiable content
✅ **Resolving ambiguities** using contextual information
✅ **Creating standalone claims** that preserve critical context
✅ **Flagging unresolvable ambiguities** instead of guessing

## Quick Start

### Installation

1. **Clone the repository:**

```bash
git clone https://github.com/TwoDigits/claimification.git
cd claimification
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Set up environment:**

```bash
cp .env.example .env
# Edit .env and add your API key:
# OPENAI_API_KEY=sk-... or ANTHROPIC_API_KEY=sk-ant-...
```

### Using as a Claude Code Plugin

```bash
# Install the plugin in Claude Code
/plugin install claimification

# Use the skill
/extract-claims
```

### Using Programmatically

```python
from src import ClaimificationPipeline

# Initialize pipeline
pipeline = ClaimificationPipeline(
    model="gpt-5-nano-2025-08-07",
    temperature=0.0
)

# Extract claims
result = pipeline.extract_claims(
    question="What are the economic challenges in Argentina?",
    answer="Argentina's inflation rate reached 25.5% monthly..."
)

# Access results
for sentence_result in result.sentence_results:
    print(f"Source: {sentence_result.source_sentence}")
    for claim in sentence_result.claims:
        print(f"  - {claim.text}")
```

### Using the CLI

```bash
python -m src.main \
    --question "What are economic challenges in Argentina?" \
    --answer "Argentina's inflation rate reached 25.5% monthly..." \
    --format markdown
```

## How It Works

Claimification uses a **4-stage pipeline**:

### Stage 1: Sentence Splitting

Splits the answer into sentences and creates rich context for each (surrounding sentences, headers, question).

### Stage 2: Selection (Verifiable Content Detection)

An LLM agent identifies sentences with verifiable content and filters out opinions, recommendations, and hypotheticals.

**Example:**

- Input: "The partnership illustrates the importance of collaboration."
- Output: ✅ Verifiable part: "There is a partnership" | ❌ Filtered: "illustrates importance"

### Stage 3: Disambiguation (Ambiguity Resolution)

An LLM agent detects ambiguous references (pronouns, time references, entities) and resolves them using context.

**Example:**

- Input: "They updated the policy next year."
- Output: ⚠️ Cannot disambiguate - unclear who "they" are and which year

### Stage 4: Decomposition (Claim Extraction)

An LLM agent breaks down sentences into atomic, standalone claims that preserve critical context.

**Example:**

- Input: "Argentina's inflation, reaching 25.5%, caused economic hardship."
- Output:
  1. "Argentina has inflation."
  2. "Argentina's inflation rate reached 25.5%."
  3. "Inflation caused economic hardship in Argentina."

## Example Output

**Question:** "What are challenges in Argentina?"

**Answer:** "Argentina's rampant inflation, with monthly rates reaching as high as 25.5%, has made many goods unobtainable and plunged the value of the currency, causing severe economic hardship."

**Extracted Claims:**

1. Argentina has rampant inflation.
2. Argentina's monthly inflation rates have reached as high as 25.5%.
3. Inflation has made many goods unobtainable in Argentina.
4. Inflation has plunged the value of Argentina's currency.
5. Inflation has caused severe economic hardship in Argentina.

## Core Principles

Claimification adheres to five key principles:

| Principle                  | Description                                                    |
| -------------------------- | -------------------------------------------------------------- |
| **Completeness**           | Captures all verifiable content, excludes unverifiable content |
| **Entailment**             | Each claim is fully supported by the source text               |
| **Standalone**             | Claims are understandable without additional context           |
| **Context Preservation**   | Critical context affecting meaning is retained                 |
| **Conservative Ambiguity** | Flags unresolvable ambiguities instead of guessing             |

See [docs/PRINCIPLES.md](docs/PRINCIPLES.md) for detailed explanations.

## Features

- 🔧 **LangChain-based Architecture** - Modular, extensible agent pipeline
- 🎯 **Structured Output** - Reliable, type-safe results using Pydantic
- 🔄 **Multi-Model Support** - Works with OpenAI (GPT-4, GPT-5-nano) and Anthropic (Claude 3.5)
- 📊 **Rich CLI Output** - Beautiful progress indicators and formatted results
- 🧪 **Comprehensive Testing** - Full test coverage for all stages
- 📝 **Excellent Documentation** - Detailed guides and examples
- 🔌 **Claude Code Integration** - Native skill for seamless workflow

## Configuration

Environment variables (see `.env.example`):

```bash
# API Keys (required - choose one)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Model Configuration
CLAIMIFICATION_MODEL=gpt-5-nano-2025-08-07
CLAIMIFICATION_TEMPERATURE=0.0
CLAIMIFICATION_MAX_TOKENS=2000

# Context Configuration
CLAIMIFICATION_CONTEXT_SENTENCES=2
CLAIMIFICATION_INCLUDE_HEADERS=true
CLAIMIFICATION_INCLUDE_QUESTION=true

# Pipeline Configuration
CLAIMIFICATION_MAX_RETRIES=3
CLAIMIFICATION_TIMEOUT_SECONDS=30
```

## Documentation

- [Installation Guide](docs/INSTALLATION.md) - Detailed setup instructions
- [Usage Guide](docs/USAGE.md) - How to use Claimification
- [API Reference](docs/API.md) - Programmatic API documentation
- [Core Principles](docs/PRINCIPLES.md) - Explanation of claim extraction principles
- [Project Structure](PROJECT_STRUCTURE.md) - Architecture and design decisions

## Use Cases

**AI Safety & Verification**

- Fact-check LLM outputs before using them in production
- Identify which claims need verification
- Integration with groundedness detection systems

**Research & Analysis**

- Extract structured claims from research summaries
- Break down complex documents into verifiable statements
- Create claim databases for meta-analysis

**Enterprise Compliance**

- Verify accuracy of AI-generated reports
- Extract auditable claims from automated summaries
- Ensure LLM outputs meet quality standards

## Development

### Run Tests

```bash
pytest tests/
```

### Run Example

```bash
python examples/basic_usage.py
```

### Project Structure

```
claimification/
├── src/                  # Source code
│   ├── stages/          # Pipeline stages
│   ├── models/          # Data models
│   ├── prompts/         # LLM prompts
│   └── utils/           # Utilities
├── skills/              # Claude Code skills
├── tests/               # Test suite
├── examples/            # Usage examples
└── docs/                # Documentation
```

## Research Foundation

This implementation is based on the paper:

> **"Towards Effective Extraction and Evaluation of Factual Claims"**

The paper demonstrates that Claimification outperforms existing LLM-based claim extraction methods:

- ✅ 99% of claims are entailed by their source sentence
- ✅ Best balance between including verifiable and excluding unverifiable content
- ✅ Least likely to omit context critical to fact-checking verdicts

## Contributing

Contributions are welcome! Please see our [Contributing Guidelines](CONTRIBUTING.md).

Areas where we'd love help:

- Additional language support
- Integration with fact-checking APIs
- Performance optimizations
- More comprehensive test cases

## Roadmap

### v1.0 (Current)

- ✅ Core 4-stage pipeline
- ✅ OpenAI & Anthropic support
- ✅ Claude Code plugin
- ✅ CLI interface
- ✅ Comprehensive documentation

### v1.1 (Planned)

- [ ] Batch processing optimization
- [ ] Caching for repeated claims
- [ ] Custom prompt templates
- [ ] Extended language support (spaCy models)

### v2.0 (Future)

- [ ] Integration with fact-checking APIs (e.g., Azure AI Groundedness)
- [ ] Claim confidence scoring
- [ ] Interactive claim review UI
- [ ] Multi-language support

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Citation

If you use Claimification in your research, please cite:

```bibtex
@software{claimification2026,
  title = {Claimification: Extract Verifiable Factual Claims from LLM Outputs},
  author = {TwoDigits},
  year = {2026},
  url = {https://github.com/TwoDigits/claimification}
}
```

## Support

- 📧 Email: info@twodigits.dev
- 🐛 Issues: [GitHub Issues](https://github.com/TwoDigits/claimification/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/TwoDigits/claimification/discussions)

## Acknowledgments

- Based on research by Microsoft Research
- Built with [LangChain](https://langchain.com/)
- Designed for [Claude Code](https://claude.ai/code)

---

**Made with ❤️ by [TwoDigits](https://twodigits.dev)**
