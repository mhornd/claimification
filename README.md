# Claimification

> **Extract verifiable factual claims and map entity relationships from text using multi-stage AI pipelines**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/LangChain-Enabled-green.svg)](https://langchain.com/)

Claimification is a Claude Code plugin providing two powerful text analysis features:

1. **Claim Extraction** - Extract verifiable factual claims using a 4-stage pipeline
2. **Entity Relationship Mapping** - Extract entities and relationships to build knowledge graphs

## Features

### 1. Claim Extraction

Extract verifiable factual claims from LLM outputs using a sophisticated 4-stage pipeline based on research from Microsoft Research.

✅ **Extracting verifiable facts** from complex LLM outputs
✅ **Filtering out opinions** and non-verifiable content
✅ **Resolving ambiguities** using contextual information
✅ **Creating standalone claims** that preserve critical context
✅ **Flagging unresolvable ambiguities** instead of guessing

### 2. Entity Relationship Mapping

Transform unstructured text into queryable knowledge graphs by extracting entities and their relationships.

📊 **Structure Chaos** - Convert LLM outputs into queryable knowledge structures
🔗 **Discover Connections** - Find both explicit and implicit relationships
🎯 **Multiple Formats** - Export as JSON or natural language summaries
🤖 **LLM-Powered Inference** - Infer implicit relationships with confidence scores

### 3. Claude Code Skills & Agent

Specialized extraction skills for analyzing communications, meetings, and documents.

📋 **Commitment extractor** - Extract promises and deadlines from any communication
✅ **Action Item Extractor** - Pull concrete to-dos with owners and timelines
🎯 **Decision extractor** - Document decisions, rationale, and alternatives
⚠️ **Risk & Liability Detector** - Identify legal risks and overpromises
🔬 **Evidence Validator** - Verify claims with rigorous internet research
🔍 **Contradiction Detector** - Find contradictory statements within texts
🤖 **Meeting Intelligence Agent** - Systematically transform meeting notes into structured minutes

## Architecture

Claimification provides multiple ways to analyze and structure text:

### MCP Servers

- **claim-extraction** - Extract verifiable claims (MCP tool)
- **entity-mapping** - Map entity relationships (MCP tool)

### Claude Code Skills

- **commitment-extractor** - Track commitments and promises
- **action-item-extractor** - Extract action items and to-dos
- **decision-extractor** - Document decisions and rationale
- **risk-liability-detector** - Identify legal risks
- **evidence-validator** - Validate claims with research
- **contradiction-detector** - Detect contradictions
- **uncertainty-quantification** - Quantify uncertainty in claims
- **audience-adapter** - Adapt content for different audiences

### Agent

- **meeting-intelligence** - Systematically process meetings using all extraction skills

All components can be used independently or together for comprehensive text analysis.

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

# Use MCP tools
/extract-claims                    # Extract verifiable claims
# extract_entities_and_relationships  # Map entity relationships (MCP tool)

# Use extraction skills
/commitment-extractor                # Track promises and commitments
/action-item-extractor            # Extract action items
/decision-extractor                 # Document decisions
/risk-liability-detector          # Identify legal risks
/evidence-validator               # Validate claims with research
/contradiction-detector           # Find contradictions

# Use the meeting intelligence agent
/meeting-intelligence             # Transform meeting notes into structured minutes
```

### Using Programmatically

```python
from src import ClaimExtractionPipeline

# Initialize pipeline
pipeline = ClaimExtractionPipeline(
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

## Claude Code Skills

Claimification includes specialized extraction skills for analyzing communications and documents:

### Core Extraction Skills

**📋 Commitment extractor** (`/commitment-extractor`)

- Extract promises, commitments, and deadlines from emails, meetings, and contracts
- Distinguish hard vs. soft commitments
- Track who committed to what by when
- Identify missing deadlines or owners

**✅ Action Item Extractor** (`/action-item-extractor`)

- Pull concrete to-dos from meetings, emails, and documents
- Identify what needs to be done, by whom, and when
- Prioritize by urgency (Urgent/High/Medium/Low)
- Flag unassigned tasks and missing deadlines

**🎯 Decision extractor** (`/decision-extractor`)

- Extract decisions and their rationale from discussions
- Document alternatives that were considered
- Track who decided what and why
- Identify open or reversed decisions

### Quality & Risk Skills

**⚠️ Risk & Liability Detector** (`/risk-liability-detector`)

- Identify legal risks and overpromises in marketing copy
- Flag missing disclaimers and regulatory violations
- Detect absolute guarantees that create liability
- Categorize risks (Legal/Regulatory/Reputational)

**🔬 Evidence Validator** (`/evidence-validator`)

- Validate factual claims with rigorous internet research
- Require double verification from reputable sources
- Assess evidence strength (Strong/Moderate/Weak/None)
- Flag unsupported claims with missing evidence

**🔍 Contradiction Detector** (`/contradiction-detector`)

- Find contradictory statements within documents
- Compare claim pairs for logical inconsistencies
- Categorize contradictions (Definite/Likely/Possible)
- Suggest fixes for identified conflicts

### Meeting Intelligence Agent

**🤖 Meeting Intelligence** (`/meeting-intelligence`)

- Systematically transform meeting notes into structured minutes
- Automatically applies relevant extraction skills:
  - Extracts decisions (via decision-extractor)
  - Identifies action items (via action-item-extractor)
  - Tracks commitments (via commitment-extractor)
  - Detects contradictions (via contradiction-detector)
  - Flags risks (via risk-liability-detector)
- Produces concise, actionable meeting minutes
- Adapts to meeting type (Strategy/Technical/Customer/Status)

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

### Claim Extraction

- [Installation Guide](docs/INSTALLATION.md) - Detailed setup instructions
- [Usage Guide](docs/USAGE.md) - How to use claim extraction
- [API Reference](docs/API.md) - Programmatic API documentation
- [Core Principles](docs/PRINCIPLES.md) - Explanation of claim extraction principles

### Entity Relationship Mapping

- [Usage Guide](docs/entity_mapping/USAGE.md) - How to use entity mapping
- [API Reference](docs/entity_mapping/API.md) - Entity mapping API documentation

### General

- [Project Structure](PROJECT_STRUCTURE.md) - Architecture and design decisions

## Use Cases

**AI Safety & Verification**

- Fact-check LLM outputs before using them in production
- Validate claims with evidence from reputable sources
- Detect contradictions in AI-generated content
- Integration with groundedness detection systems

**Meeting & Communication Management**

- Transform meeting notes into actionable minutes
- Track commitments and promises automatically
- Extract action items with owners and deadlines
- Document decisions and rationale for future reference

**Legal & Compliance**

- Identify legal risks in marketing copy and contracts
- Flag overpromises and missing disclaimers
- Ensure regulatory compliance in customer communications
- Validate factual claims before publication

**Research & Analysis**

- Extract structured claims from research summaries
- Validate claims with rigorous evidence checking
- Build knowledge graphs from unstructured text
- Create claim databases for meta-analysis

**Enterprise Workflows**

- Verify accuracy of AI-generated reports
- Extract auditable claims from automated summaries
- Structure chaos from brainstorming sessions
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
├── src/                           # Source code
│   ├── stages/                   # Pipeline stages
│   ├── models/                   # Data models
│   ├── prompts/                  # LLM prompts
│   └── utils/                    # Utilities
├── skills/                        # Claude Code skills
│   ├── commitment-extractor/       # Track promises and commitments
│   ├── action-item-extractor/    # Extract action items
│   ├── decision-extractor/         # Document decisions
│   ├── risk-liability-detector/  # Identify legal risks
│   ├── evidence-validator/       # Validate claims
│   ├── contradiction-detector/   # Find contradictions
│   ├── uncertainty-quantification/ # Quantify uncertainty
│   ├── audience-adapter/         # Adapt content
│   └── meeting-intelligence/     # Meeting analysis agent
├── commands/                      # Skill command wrappers
├── agents/                        # Agent configurations
├── tests/                         # Test suite
├── examples/                      # Usage examples
└── docs/                          # Documentation
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
