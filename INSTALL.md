# Installation Methods

This document describes different ways to install and use Claimification.

## Method 1: Local Development (Recommended for Development)

Best for: Contributing, testing, or modifying the code.

```bash
# Clone repository
git clone https://github.com/TwoDigits/claimification.git
cd claimification

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env and add your API key

# Run directly
python -m src.main --question "Your question" --answer "Your answer"
```

**Import in Python:**

```python
from src import ClaimificationPipeline
```

---

## Method 2: Pip Install (Recommended for Production)

Best for: Using Claimification in your projects.

```bash
# Install from GitHub
pip install git+https://github.com/TwoDigits/claimification.git

# Or install from local clone
cd claimification
pip install .

# Or install in editable mode for development
pip install -e .
```

**After pip install, you can:**

1. **Use the command:**

```bash
claimification --question "Your question" --answer "Your answer"
```

2. **Import in Python:**

```python
from src import ClaimificationPipeline
```

**Note:** The package installs as "claimification" but the Python module remains "src" for imports.

---

## Method 3: Claude Code Plugin

Best for: Using with Claude Code in your development workflow.

```bash
# Install plugin in Claude Code
/plugin install TwoDigits/claimification

# Or from TwoDigits Marketplace
/plugin install claimification@twodigits-marketplace

# Use the skill
/extract-claims
```

---

## Package Structure Explanation

Claimification uses a common pattern where:

- **Package name:** `claimification` (for pip install, command line)
- **Module name:** `src` (for Python imports)

This is intentional to maintain consistency with the source code structure while providing a user-friendly package name.

**Examples:**

```python
# ✅ Correct - always use src for imports
from src import ClaimificationPipeline
from src.models import Claim, SentenceStatus

# ❌ Incorrect - this won't work
from claimification import ClaimificationPipeline  # Won't work!
```

**Command Line:**

```bash
# ✅ After pip install
claimification --question "..." --answer "..."

# ✅ Direct module execution (without install)
python -m src.main --question "..." --answer "..."

# ✅ Python script
python examples/basic_usage.py
```

---

## Environment Setup

All methods require an API key. Set one of:

```bash
# OpenAI (recommended)
export OPENAI_API_KEY=sk-proj-...

# Or Anthropic
export ANTHROPIC_API_KEY=sk-ant-...

# Optional configuration
export CLAIMIFICATION_MODEL=gpt-5-nano-2025-08-07
export CLAIMIFICATION_TEMPERATURE=0.0
export CLAIMIFICATION_CONTEXT_SENTENCES=2
```

Or use a `.env` file:

```bash
cp .env.example .env
# Edit .env with your API keys
```

---

## Verification

Test your installation:

```bash
# Method 1 & 2: Run example
python examples/basic_usage.py

# Method 2: Use command
claimification --help

# Method 3: Use Claude Code skill
/extract-claims
```

---

## Troubleshooting

### Import Error: "No module named 'src'"

**Solution:** Make sure you're in the project directory or have installed with pip.

```bash
# Check current directory
pwd

# Or add to Python path
export PYTHONPATH="${PYTHONPATH}:/path/to/claimification"

# Or install with pip
pip install -e .
```

### Command not found: "claimification"

**Solution:** Install the package with pip:

```bash
pip install .
# Or
pip install git+https://github.com/TwoDigits/claimification.git
```

### API Key Error

**Solution:** Set environment variable or use .env file:

```bash
export OPENAI_API_KEY=sk-proj-your-key-here
```

---

## Next Steps

- Read [USAGE.md](docs/USAGE.md) for detailed usage instructions
- See [examples/](examples/) for code examples
- Check [QUICKSTART.md](QUICKSTART.md) for quick reference
