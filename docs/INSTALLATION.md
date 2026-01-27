# Installation Guide

This guide covers different installation methods for Claimification.

## Prerequisites

- **Python 3.10 or higher**
- **pip** (Python package manager)
- **API Key** from OpenAI or Anthropic

## Method 1: Standalone Installation

### 1. Clone the Repository

```bash
git clone https://github.com/TwoDigits/claimification.git
cd claimification
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your API key
nano .env  # or your preferred editor
```

Add one of these to your `.env`:
```bash
OPENAI_API_KEY=sk-proj-...
# OR
ANTHROPIC_API_KEY=sk-ant-...
```

### 5. Verify Installation

```bash
python examples/basic_usage.py
```

## Method 2: Claude Code Plugin

### 1. Install via Claude Code

```bash
# From TwoDigits Marketplace
/plugin install claimification@twodigits-marketplace

# Or directly from repository
/plugin install TwoDigits/claimification
```

### 2. Configure API Key

```bash
# Add to your shell profile (~/.bashrc, ~/.zshrc, etc.)
export OPENAI_API_KEY=sk-proj-...
# OR
export ANTHROPIC_API_KEY=sk-ant-...
```

### 3. Verify Installation

```bash
/extract-claims
```

## Method 3: Development Installation

For contributors and developers:

### 1. Clone and Setup

```bash
git clone https://github.com/TwoDigits/claimification.git
cd claimification
python -m venv venv
source venv/bin/activate
```

### 2. Install in Editable Mode

```bash
pip install -e .
pip install -r requirements.txt
```

### 3. Install Development Dependencies

```bash
pip install pytest pytest-asyncio black mypy
```

### 4. Run Tests

```bash
pytest tests/
```

## API Key Setup

### OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Create a new API key
3. Add to `.env` or export as environment variable

**Supported Models:**
- `gpt-4o` (recommended)
- `gpt-4`
- `gpt-3.5-turbo`

### Anthropic API Key

1. Go to https://console.anthropic.com/
2. Create a new API key
3. Add to `.env` or export as environment variable

**Supported Models:**
- `claude-3-5-sonnet-20241022` (recommended)
- `claude-3-opus-20240229`

## Optional: spaCy Language Model

For more robust sentence splitting, install a spaCy model:

```bash
python -m spacy download en_core_web_sm
```

Update `src/stages/sentence_splitter.py` to use spaCy instead of regex.

## Troubleshooting

### "Module not found" Error

Make sure you're in the correct directory and virtual environment is activated:
```bash
pwd  # Should show .../claimification
which python  # Should show venv/bin/python
```

### API Key Not Found

Verify environment variable is set:
```bash
echo $OPENAI_API_KEY  # or $ANTHROPIC_API_KEY
```

If using `.env` file, make sure it's in the project root:
```bash
ls -la .env
```

### Import Error with LangChain

Reinstall dependencies:
```bash
pip install --upgrade -r requirements.txt
```

### Rate Limit Errors

Reduce concurrent requests or use a higher tier API plan.

## Next Steps

- Read [USAGE.md](USAGE.md) for usage instructions
- Check [API.md](API.md) for programmatic usage
- See [examples/](../examples/) for code examples
