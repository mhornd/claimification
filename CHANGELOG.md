# Changelog

All notable changes to Claimification will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-27

### Added

#### Core Pipeline
- 4-stage claim extraction pipeline (Sentence Splitting, Selection, Disambiguation, Decomposition)
- LangChain integration with structured output using Pydantic models
- Multi-model support for OpenAI (GPT-4, GPT-4o, GPT-3.5-turbo) and Anthropic (Claude 3.5 Sonnet, Claude 3 Opus)
- Type-safe data models using Pydantic
- Automatic retry logic for LLM API failures
- Context-aware sentence processing with configurable window size

#### Stage 1: Sentence Splitter
- Regex-based sentence splitting
- Markdown header extraction and hierarchy tracking
- Context builder with surrounding sentences
- Metadata extraction (position, headers, paragraph numbers)

#### Stage 2: Selection Agent
- LLM-powered verifiable content detection
- Sentence rewriting for partially verifiable content
- Opinion and recommendation filtering
- Detailed reasoning for decisions

#### Stage 3: Disambiguation Agent
- Pronoun, temporal, and entity ambiguity detection
- Context-based ambiguity resolution
- Conservative approach to unresolvable ambiguities
- Detailed ambiguity explanations

#### Stage 4: Decomposition Agent
- Atomic claim extraction
- Context preservation in claims
- Standalone claim generation
- Entailment checking

#### Interfaces
- Python API with `ClaimificationPipeline` class
- Command-line interface with argparse
- Claude Code skill integration (`/extract-claims`)
- Rich CLI output with progress bars and colored text
- Markdown and JSON export formats

#### Documentation
- Comprehensive README with quick start guide
- Installation guide (docs/INSTALLATION.md)
- Usage guide (docs/USAGE.md)
- Quick start guide (QUICKSTART.md)
- Project structure documentation (PROJECT_STRUCTURE.md)
- Verification document (VERIFICATION.md)

#### Configuration
- Environment variable configuration
- `.env.example` template
- Configurable LLM model selection
- Adjustable temperature and context window
- Customizable retry behavior

#### Development
- Python package structure with `pyproject.toml`
- Requirements file with core and dev dependencies
- Example usage script (examples/basic_usage.py)
- MIT License
- GitHub-ready repository structure

#### Marketplace
- Claude Code plugin manifest (.claude-plugin/plugin.json)
- Marketplace metadata file (marketplace-metadata.json)
- TwoDigits Marketplace compatibility
- Professional documentation and metadata

### Research Foundation
- Based on "Towards Effective Extraction and Evaluation of Factual Claims" paper
- 99% claim entailment accuracy
- Best balance for verifiable/unverifiable content
- Minimal critical context omission

---

## [Unreleased]

### Planned for v1.1
- Batch processing optimization for parallel sentence processing
- Caching mechanism for repeated claim patterns
- Custom prompt template support
- Extended language support with spaCy models
- Performance metrics and logging

### Planned for v2.0
- Integration with fact-checking APIs (Azure AI Groundedness Detection)
- Claim confidence scoring
- Interactive claim review UI (Streamlit/Gradio)
- Multi-language support
- Graph-based claim relationships
- Claim deduplication
- Export to knowledge graph formats

---

## Version History

- **v1.0.0** (2026-01-27) - Initial release with full 4-stage pipeline, multi-model support, and marketplace integration
