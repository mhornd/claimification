# Contributing to Claimification

Thank you for your interest in contributing to Claimification! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

We are committed to providing a welcoming and inclusive environment. Please:

- Be respectful and considerate in communication
- Accept constructive criticism gracefully
- Focus on what's best for the project and community
- Show empathy towards other contributors

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Git
- OpenAI or Anthropic API key
- Basic knowledge of LangChain and Pydantic

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/claimification.git
   cd claimification
   ```

## Development Setup

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
# Core dependencies
pip install -r requirements.txt

# Development dependencies
pip install pytest pytest-asyncio black mypy
```

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env and add your API key
```

### 4. Verify Setup

```bash
# Run example
python examples/basic_usage.py

# Run tests (when available)
pytest tests/
```

## How to Contribute

### Areas We'd Love Help With

1. **Testing**
   - Write unit tests for pipeline stages
   - Add integration tests
   - Create test fixtures with diverse examples

2. **Documentation**
   - Improve installation instructions
   - Add more usage examples
   - Translate documentation to other languages

3. **Features**
   - Batch processing optimization
   - Additional LLM provider support
   - Caching mechanism
   - Performance improvements

4. **Integration**
   - Fact-checking API integrations
   - Web UI (Streamlit/Gradio)
   - CI/CD pipeline setup

5. **Bug Fixes**
   - Fix reported issues
   - Improve error handling
   - Edge case handling

## Coding Standards

### Python Style Guide

We follow PEP 8 with some modifications:

- **Line Length**: 100 characters (not 79)
- **Formatter**: Black
- **Type Hints**: Use type hints where possible
- **Docstrings**: Google-style docstrings

### Code Formatting

Format your code with Black:

```bash
black src/ tests/
```

### Type Checking

Run mypy for type checking:

```bash
mypy src/
```

### Example Code Style

```python
"""Module docstring explaining purpose."""

from typing import List, Optional
from pydantic import BaseModel


class ExampleModel(BaseModel):
    """Model docstring.

    Attributes:
        field_name: Description of field
    """
    field_name: str


def example_function(param: str, optional_param: Optional[int] = None) -> List[str]:
    """Function doing something.

    Args:
        param: Description of param
        optional_param: Description of optional param

    Returns:
        List of strings

    Raises:
        ValueError: When param is invalid
    """
    if not param:
        raise ValueError("param cannot be empty")

    # Implementation
    results = []
    # ...
    return results
```

## Testing

### Writing Tests

- Create test files in `tests/` directory
- Name test files `test_*.py`
- Name test functions `test_*`
- Use descriptive test names

### Test Structure

```python
import pytest
from src.pipeline import ClaimificationPipeline


def test_pipeline_initialization():
    """Test that pipeline initializes correctly."""
    pipeline = ClaimificationPipeline()
    assert pipeline is not None
    assert pipeline.model_name == "gpt-5-nano-2025-08-07"


def test_claim_extraction_basic():
    """Test basic claim extraction."""
    pipeline = ClaimificationPipeline()
    result = pipeline.extract_claims(
        question="What is Python?",
        answer="Python is a programming language."
    )
    assert len(result.sentence_results) > 0
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_pipeline.py

# Run with coverage
pytest --cov=src tests/
```

## Documentation

### Docstring Format

Use Google-style docstrings:

```python
def function_name(param1: str, param2: int) -> bool:
    """Short description of function.

    Longer description if needed, explaining the purpose
    and behavior in more detail.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: When param1 is invalid
        TypeError: When param2 is not an integer

    Example:
        >>> function_name("test", 42)
        True
    """
```

### README Updates

When adding features, update:

- Main README.md with feature description
- Usage examples in docs/USAGE.md
- Installation instructions if new dependencies added

## Pull Request Process

### Before Submitting

1. **Create a Branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**
   - Write code following our standards
   - Add tests for new functionality
   - Update documentation

3. **Test Your Changes**

   ```bash
   pytest tests/
   black src/ tests/
   mypy src/
   ```

4. **Commit**
   ```bash
   git add .
   git commit -m "Add feature: your feature description"
   ```

### Commit Message Format

Use clear, descriptive commit messages:

```
Add feature: brief description

Longer explanation of what changed and why.
Include any breaking changes or important notes.

Fixes #123
```

**Types of commits:**

- `Add feature:` - New functionality
- `Fix:` - Bug fixes
- `Update:` - Updates to existing features
- `Refactor:` - Code refactoring
- `Docs:` - Documentation changes
- `Test:` - Test additions or changes
- `Style:` - Code style changes (formatting, etc.)

### Submit Pull Request

1. **Push to Your Fork**

   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create PR on GitHub**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your branch
   - Fill in the PR template

3. **PR Description Should Include:**
   - What changed and why
   - Any breaking changes
   - Related issue numbers (Fixes #123)
   - Screenshots if UI changes
   - Testing done

### PR Review Process

- Maintainers will review your PR
- Address any requested changes
- Once approved, it will be merged

## Questions?

- 📧 Email: info@twodigits.dev
- 💬 Discussions: [GitHub Discussions](https://github.com/TwoDigits/claimification/discussions)
- 🐛 Issues: [GitHub Issues](https://github.com/TwoDigits/claimification/issues)

## Thank You!

Your contributions make Claimification better for everyone. We appreciate your time and effort! 🎉
