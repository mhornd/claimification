# Marketplace Package Restructure Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Restructure claimification package for pip-installable marketplace distribution with proper namespace and MCP server entry points.

**Architecture:** Transform flat `src/` structure to nested `src/claimification/` namespace package. Move MCP servers inside package. Update all imports from `from src.` to `from claimification.`. Add console script entry points for MCP servers. Maintain backward compatibility via package exports.

**Tech Stack:** Python 3.10+, setuptools, pyproject.toml, MCP SDK

---

## Task 1: Create New Package Structure

**Files:**
- Create: `src/claimification/__init__.py`
- Create: `src/claimification/mcp_servers/__init__.py`

**Step 1: Create nested package directory**

```bash
mkdir -p src/claimification/mcp_servers
```

**Step 2: Create package __init__.py**

In `src/claimification/__init__.py`:
```python
"""Claimification - Extract verifiable factual claims and map entity relationships.

This package provides:
1. Claim Extraction - Multi-stage pipeline for extracting verifiable factual claims
2. Entity Mapping - Extract entities and relationships to build knowledge graphs
"""

from claimification.claim_extraction import (
    ClaimExtractionPipeline,
    Claim,
    PipelineResult,
    ClaimExtractionResult,
    SentenceStatus
)

from claimification.entity_mapping import (
    EntityMappingPipeline,
    Entity,
    EntityType,
    Relationship,
    KnowledgeGraph,
    GraphMetadata
)

__version__ = "2.1.0"
__author__ = "TwoDigits"

__all__ = [
    "ClaimExtractionPipeline",
    "Claim",
    "PipelineResult",
    "ClaimExtractionResult",
    "SentenceStatus",
    "EntityMappingPipeline",
    "Entity",
    "EntityType",
    "Relationship",
    "KnowledgeGraph",
    "GraphMetadata",
]
```

**Step 3: Create MCP servers __init__.py**

In `src/claimification/mcp_servers/__init__.py`:
```python
"""MCP Servers for Claude Code integration."""

__all__ = []
```

**Step 4: Verify directory structure**

Run: `ls -la src/claimification/`
Expected: Shows `__init__.py` and `mcp_servers/`

**Step 5: Commit structure setup**

```bash
git add src/claimification/
git commit -m "feat: create claimification package namespace structure"
```

---

## Task 2: Move Claim Extraction Module

**Files:**
- Move: `src/claim_extraction/` → `src/claimification/claim_extraction/`

**Step 1: Move claim_extraction directory**

```bash
mv src/claim_extraction src/claimification/
```

**Step 2: Update claim_extraction/__init__.py imports**

In `src/claimification/claim_extraction/__init__.py`, replace:
```python
from src.claim_extraction.pipeline import ClaimExtractionPipeline
from src.claim_extraction.models import (
```

With:
```python
from claimification.claim_extraction.pipeline import ClaimExtractionPipeline
from claimification.claim_extraction.models import (
```

**Step 3: Update claim_extraction/pipeline.py imports**

Find all lines with `from src.claim_extraction` and replace with `from claimification.claim_extraction`

Run: `grep -n "from src\." src/claimification/claim_extraction/pipeline.py`

**Step 4: Update models/__init__.py imports**

In `src/claimification/claim_extraction/models/__init__.py`, replace `from src.` with `from claimification.`

**Step 5: Update all stage files imports**

For each file in `src/claimification/claim_extraction/stages/`:
- Replace `from src.claim_extraction` with `from claimification.claim_extraction`

**Step 6: Verify imports work**

Run: `python -c "from claimification.claim_extraction import ClaimExtractionPipeline; print('OK')"`
Expected: "OK"

**Step 7: Commit claim extraction migration**

```bash
git add src/claimification/claim_extraction/
git commit -m "refactor: migrate claim_extraction to claimification namespace"
```

---

## Task 3: Move Entity Mapping Module

**Files:**
- Move: `src/entity_mapping/` → `src/claimification/entity_mapping/`

**Step 1: Move entity_mapping directory**

```bash
mv src/entity_mapping src/claimification/
```

**Step 2: Update entity_mapping/__init__.py imports**

In `src/claimification/entity_mapping/__init__.py`, replace:
```python
from src.entity_mapping.pipeline import EntityMappingPipeline
from src.entity_mapping.models import (
```

With:
```python
from claimification.entity_mapping.pipeline import EntityMappingPipeline
from claimification.entity_mapping.models import (
```

**Step 3: Update entity_mapping/pipeline.py imports**

Find and replace all `from src.entity_mapping` with `from claimification.entity_mapping`

Run: `grep -n "from src\." src/claimification/entity_mapping/pipeline.py`

**Step 4: Update models imports**

In `src/claimification/entity_mapping/models/*.py`, replace `from src.` with `from claimification.`

**Step 5: Update all stage files imports**

For each file in `src/claimification/entity_mapping/stages/`:
- Replace `from src.entity_mapping` with `from claimification.entity_mapping`

**Step 6: Verify imports work**

Run: `python -c "from claimification.entity_mapping import EntityMappingPipeline; print('OK')"`
Expected: "OK"

**Step 7: Commit entity mapping migration**

```bash
git add src/claimification/entity_mapping/
git commit -m "refactor: migrate entity_mapping to claimification namespace"
```

---

## Task 4: Move Utils Module

**Files:**
- Move: `src/utils/` → `src/claimification/utils/`

**Step 1: Move utils directory**

```bash
mv src/utils src/claimification/
```

**Step 2: Update utils imports if any**

In `src/claimification/utils/__init__.py`, replace any `from src.` with `from claimification.`

**Step 3: Find files that import utils**

Run: `grep -r "from src.utils" src/claimification/`

**Step 4: Update all utils imports**

Replace `from src.utils` with `from claimification.utils` in all files found above.

**Step 5: Verify utils imports**

Run: `python -c "from claimification.utils import *; print('OK')"`
Expected: Either "OK" or specific import error if utils has specific exports

**Step 6: Commit utils migration**

```bash
git add src/claimification/utils/
git commit -m "refactor: migrate utils to claimification namespace"
```

---

## Task 5: Migrate Claim Extraction MCP Server

**Files:**
- Move: `mcp_servers/claim_extraction_server.py` → `src/claimification/mcp_servers/claim_extraction_server.py`
- Modify: `src/claimification/mcp_servers/claim_extraction_server.py` (update imports)

**Step 1: Copy MCP server to new location**

```bash
cp mcp_servers/claim_extraction_server.py src/claimification/mcp_servers/
```

**Step 2: Update imports in claim_extraction_server.py**

Replace lines 27-28:
```python
from src.claim_extraction.pipeline import ClaimExtractionPipeline
from src.claim_extraction.models import PipelineResult
```

With:
```python
from claimification.claim_extraction.pipeline import ClaimExtractionPipeline
from claimification.claim_extraction.models import PipelineResult
```

**Step 3: Ensure main() function is properly defined**

Verify that `async def main():` exists at line 217 and is the entry point.

**Step 4: Test server can be imported**

Run: `python -c "from claimification.mcp_servers.claim_extraction_server import main; print('OK')"`
Expected: "OK"

**Step 5: Commit MCP server migration**

```bash
git add src/claimification/mcp_servers/claim_extraction_server.py
git commit -m "refactor: migrate claim extraction MCP server to package"
```

---

## Task 6: Migrate Entity Mapping MCP Server

**Files:**
- Move: `mcp_servers/entity_mapping_server.py` → `src/claimification/mcp_servers/entity_mapping_server.py`
- Modify: `src/claimification/mcp_servers/entity_mapping_server.py` (update imports)

**Step 1: Copy MCP server to new location**

```bash
cp mcp_servers/entity_mapping_server.py src/claimification/mcp_servers/
```

**Step 2: Update imports in entity_mapping_server.py**

Replace line 27:
```python
from src.entity_mapping import EntityMappingPipeline, KnowledgeGraph
```

With:
```python
from claimification.entity_mapping import EntityMappingPipeline, KnowledgeGraph
```

**Step 3: Verify main() function exists**

Check that `async def main():` exists at line 191 as the entry point.

**Step 4: Test server can be imported**

Run: `python -c "from claimification.mcp_servers.entity_mapping_server import main; print('OK')"`
Expected: "OK"

**Step 5: Commit MCP server migration**

```bash
git add src/claimification/mcp_servers/entity_mapping_server.py
git commit -m "refactor: migrate entity mapping MCP server to package"
```

---

## Task 7: Update Main CLI Entry Point

**Files:**
- Move: `src/main.py` → `src/claimification/cli.py`
- Modify: `src/claimification/cli.py` (update imports)

**Step 1: Copy main.py to new location**

```bash
cp src/main.py src/claimification/cli.py
```

**Step 2: Update imports in cli.py**

Find all lines starting with `from src.` and replace with `from claimification.`

Run: `grep -n "^from src\." src/claimification/cli.py`

Replace each occurrence.

**Step 3: Verify CLI imports work**

Run: `python -c "from claimification.cli import main; print('OK')"`
Expected: "OK"

**Step 4: Test CLI runs**

Run: `python -m claimification.cli --help`
Expected: Shows help message

**Step 5: Commit CLI migration**

```bash
git add src/claimification/cli.py
git commit -m "refactor: migrate CLI to claimification.cli"
```

---

## Task 8: Update pyproject.toml Configuration

**Files:**
- Modify: `pyproject.toml` (lines 64-68)

**Step 1: Update project.scripts section**

Replace lines 64-65:
```toml
[project.scripts]
claimification = "src.main:main"
```

With:
```toml
[project.scripts]
claimification = "claimification.cli:main"
claimification-claim-extraction = "claimification.mcp_servers.claim_extraction_server:main"
claimification-entity-mapping = "claimification.mcp_servers.entity_mapping_server:main"
```

**Step 2: Update tool.setuptools section**

Replace lines 67-68:
```toml
[tool.setuptools]
packages = ["src", "src.stages", "src.models", "src.prompts", "src.utils"]
```

With:
```toml
[tool.setuptools]
package-dir = {"" = "src"}

[tool.setuptools.packages.find]
where = ["src"]
include = ["claimification*"]
```

**Step 3: Remove old package-data if not needed**

Check line 70-71. If `src.py.typed` doesn't exist, remove or update to `claimification.py.typed`.

**Step 4: Verify pyproject.toml syntax**

Run: `python -c "import tomli; tomli.load(open('pyproject.toml', 'rb'))"`
Expected: No syntax errors

**Step 5: Commit pyproject.toml updates**

```bash
git add pyproject.toml
git commit -m "build: update pyproject.toml for claimification namespace package"
```

---

## Task 9: Update Marketplace Metadata

**Files:**
- Modify: `marketplace-metadata.json` (lines 68-76)

**Step 1: Update MCP server entry points**

Replace lines 68-76:
```json
  "mcpServers": {
    "claimification": {
      "command": "python",
      "args": ["mcp_server.py"],
      "env": {
        "OPENAI_API_KEY": "${OPENAI_API_KEY}"
      }
    }
  },
```

With:
```json
  "mcpServers": {
    "claim-extraction": {
      "command": "claimification-claim-extraction",
      "env": {
        "OPENAI_API_KEY": "${OPENAI_API_KEY}"
      }
    },
    "entity-mapping": {
      "command": "claimification-entity-mapping",
      "env": {
        "OPENAI_API_KEY": "${OPENAI_API_KEY}"
      }
    }
  },
```

**Step 2: Update installation command**

Replace line 78:
```json
    "command": "pip install -r requirements.txt",
```

With:
```json
    "command": "pip install .",
```

**Step 3: Update version to 2.1.0**

Change line 4:
```json
  "version": "2.0.2",
```

To:
```json
  "version": "2.1.0",
```

**Step 4: Verify JSON syntax**

Run: `python -c "import json; json.load(open('marketplace-metadata.json'))"`
Expected: No syntax errors

**Step 5: Commit metadata updates**

```bash
git add marketplace-metadata.json
git commit -m "build: update marketplace metadata for new entry points"
```

---

## Task 10: Update Test Imports

**Files:**
- Modify: `tests/test_imports.py`
- Modify: Other test files as needed

**Step 1: Find all test files with src imports**

Run: `grep -r "from src\." tests/`

**Step 2: Update test_imports.py**

Replace all `from src.` with `from claimification.` in tests/test_imports.py

**Step 3: Update other test files**

For each file found in step 1, replace `from src.` with `from claimification.`

**Step 4: Run tests to verify**

Run: `pytest tests/ -v`
Expected: All tests pass (or same pass/fail status as before)

**Step 5: Commit test updates**

```bash
git add tests/
git commit -m "test: update imports to claimification namespace"
```

---

## Task 11: Create Backward Compatibility Shim

**Files:**
- Create: `src/__init__.py` (deprecation warnings)

**Step 1: Write backward compatibility __init__.py**

In `src/__init__.py`:
```python
"""Backward compatibility shim for old 'src' imports.

DEPRECATED: Import from 'claimification' instead.
"""

import warnings

warnings.warn(
    "Importing from 'src' is deprecated and will be removed in version 3.0. "
    "Please update imports to use 'claimification' instead:\n"
    "  from claimification.claim_extraction import ClaimExtractionPipeline\n"
    "  from claimification.entity_mapping import EntityMappingPipeline",
    DeprecationWarning,
    stacklevel=2
)

# Re-export from new location for backward compatibility
from claimification import *  # noqa: F401, F403

__all__ = [
    "ClaimExtractionPipeline",
    "Claim",
    "PipelineResult",
    "ClaimExtractionResult",
    "SentenceStatus",
    "EntityMappingPipeline",
    "Entity",
    "EntityType",
    "Relationship",
    "KnowledgeGraph",
    "GraphMetadata",
]
```

**Step 2: Test backward compatibility**

Run: `python -c "from src.claim_extraction import ClaimExtractionPipeline; print('OK')"`
Expected: DeprecationWarning + "OK"

**Step 3: Verify warning is shown**

Run: `python -W default -c "from src.claim_extraction import ClaimExtractionPipeline"`
Expected: Shows deprecation warning

**Step 4: Commit backward compatibility layer**

```bash
git add src/__init__.py
git commit -m "feat: add backward compatibility shim for old src imports"
```

---

## Task 12: Test Package Installation

**Files:**
- Test: Local editable install

**Step 1: Create test virtual environment**

```bash
python -m venv test_venv
source test_venv/bin/activate  # On Windows: test_venv\Scripts\activate
```

**Step 2: Install package in editable mode**

Run: `pip install -e .`
Expected: Package installs successfully

**Step 3: Test entry points are installed**

Run: `which claimification-claim-extraction`
Expected: Shows path to installed script

Run: `which claimification-entity-mapping`
Expected: Shows path to installed script

**Step 4: Test Python imports**

Run:
```bash
python -c "from claimification import ClaimExtractionPipeline, EntityMappingPipeline; print('OK')"
```
Expected: "OK"

**Step 5: Test CLI works**

Run: `claimification --help`
Expected: Shows help message

**Step 6: Deactivate and remove test env**

```bash
deactivate
rm -rf test_venv
```

**Step 7: Document test results**

Create note in commit message about successful installation test.

**Step 8: Commit testing documentation**

```bash
git add .
git commit --allow-empty -m "test: verify package installation and entry points"
```

---

## Task 13: Update Documentation

**Files:**
- Modify: `README.md`
- Modify: `INSTALL.md`
- Modify: `docs/` files as needed

**Step 1: Update README.md installation instructions**

Find installation section and ensure it shows:
```bash
pip install claimification
```

**Step 2: Update README.md import examples**

Replace any `from src.` examples with `from claimification.`

**Step 3: Update INSTALL.md**

Update any references to package structure or imports from `src.` to `claimification.`

**Step 4: Update docs/ files**

Run: `grep -r "from src\." docs/`

Replace all occurrences with `from claimification.`

**Step 5: Add migration guide**

Create `docs/MIGRATION.md` with upgrade instructions:
```markdown
# Migration Guide: v2.0 → v2.1

## What Changed

Version 2.1.0 restructures the package for proper pip installation:
- Package renamed from `src` to `claimification`
- MCP servers now installed as console scripts

## Update Your Code

**Old (v2.0):**
```python
from src.claim_extraction import ClaimExtractionPipeline
```

**New (v2.1):**
```python
from claimification.claim_extraction import ClaimExtractionPipeline
```

## MCP Server Configuration

**Old:**
```json
{
  "command": "python",
  "args": ["path/to/mcp_server.py"]
}
```

**New:**
```json
{
  "command": "claimification-claim-extraction"
}
```

No path needed - commands are globally available after `pip install`.
```

**Step 6: Verify all docs updated**

Run: `grep -r "from src\." . --exclude-dir=.git --exclude-dir=venv --exclude-dir=test_venv`
Expected: Only finds files in old `mcp_servers/` or other archived locations

**Step 7: Commit documentation updates**

```bash
git add README.md INSTALL.md docs/
git commit -m "docs: update for claimification namespace package"
```

---

## Task 14: Clean Up Old Files

**Files:**
- Remove: `mcp_servers/` (old location)
- Remove: `src/main.py` (moved to cli.py)
- Archive: Keep originals for reference if needed

**Step 1: Verify new structure works**

Run: `python -c "from claimification.mcp_servers.claim_extraction_server import main; print('OK')"`
Expected: "OK"

**Step 2: Remove old mcp_servers directory**

```bash
git rm -r mcp_servers/
```

**Step 3: Remove old main.py**

```bash
git rm src/main.py
```

**Step 4: Verify package still works**

Run: `pytest tests/ -v`
Expected: All tests pass

**Step 5: Commit cleanup**

```bash
git commit -m "refactor: remove old mcp_servers and src/main.py"
```

---

## Task 15: Update README with Entry Point Usage

**Files:**
- Modify: `README.md` (add MCP server usage section)

**Step 1: Add MCP server configuration section**

Add to README.md after installation:
```markdown
## MCP Server Configuration

After installation, configure Claude Code to use the MCP servers:

**In `~/.config/claude-code/mcp_settings.json`:**

```json
{
  "mcpServers": {
    "claimification-claim-extraction": {
      "command": "claimification-claim-extraction",
      "env": {
        "OPENAI_API_KEY": "your-api-key-here"
      }
    },
    "claimification-entity-mapping": {
      "command": "claimification-entity-mapping",
      "env": {
        "OPENAI_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

**Environment Variables:**
- Set `OPENAI_API_KEY` in your environment or `.env` file
- Alternatively set `ANTHROPIC_API_KEY` for Claude models

**Verify Installation:**
```bash
which claimification-claim-extraction
which claimification-entity-mapping
```

Both commands should show installed script paths.
```

**Step 2: Add example usage section**

```markdown
## Quick Start

### Python API
```python
from claimification import ClaimExtractionPipeline

pipeline = ClaimExtractionPipeline(model="gpt-4o-mini")
result = pipeline.extract_claims("The Earth orbits the Sun.")
print(result.get_all_claims())
```

### CLI
```bash
claimification --help
```

### In Claude Code
After configuring MCP servers, use the tools:
- `extract_claims` - Extract verifiable claims
- `extract_entities_and_relationships` - Build knowledge graphs
```

**Step 3: Verify README formatting**

Run: `cat README.md | head -50`
Expected: Shows updated content

**Step 4: Commit README updates**

```bash
git add README.md
git commit -m "docs: add MCP server configuration and usage guide"
```

---

## Task 16: Create GitHub Release Notes

**Files:**
- Create: `RELEASE_NOTES_v2.1.0.md`

**Step 1: Write release notes**

Create `RELEASE_NOTES_v2.1.0.md`:
```markdown
# Release Notes: v2.1.0 - Marketplace Ready Package

## 🎉 Major Improvements

### Proper Package Structure
- **Namespace Package**: Restructured from `src` to `claimification`
- **Pip Installable**: Can now be installed via `pip install claimification`
- **Entry Points**: MCP servers installed as global console commands

### MCP Server Integration
- **No Path Configuration**: Servers available as `claimification-claim-extraction` and `claimification-entity-mapping`
- **Simplified Config**: Just specify command name, no Python paths needed
- **Environment Variables**: Automatic `.env` file loading

### Breaking Changes

⚠️ **Import Path Change**
```python
# Old (v2.0)
from src.claim_extraction import ClaimExtractionPipeline

# New (v2.1)
from claimification.claim_extraction import ClaimExtractionPipeline
```

**Backward Compatibility**: Old imports still work but show deprecation warnings.

⚠️ **MCP Server Configuration**
```json
// Old
{"command": "python", "args": ["path/to/server.py"]}

// New
{"command": "claimification-claim-extraction"}
```

### Migration Guide
See [MIGRATION.md](docs/MIGRATION.md) for detailed upgrade instructions.

## Installation

```bash
pip install claimification
```

## What's Next (v2.2)
- Remove backward compatibility shim (v3.0)
- Add type stubs (py.typed)
- Performance optimizations
```

**Step 2: Verify formatting**

Run: `cat RELEASE_NOTES_v2.1.0.md`
Expected: Shows formatted release notes

**Step 3: Commit release notes**

```bash
git add RELEASE_NOTES_v2.1.0.md
git commit -m "docs: add v2.1.0 release notes"
```

---

## Task 17: Final Verification and Testing

**Files:**
- Test: All entry points
- Test: Import paths
- Test: MCP servers

**Step 1: Clean install test**

```bash
python -m venv fresh_test_venv
source fresh_test_venv/bin/activate
pip install .
```

**Step 2: Test all entry points exist**

```bash
which claimification
which claimification-claim-extraction
which claimification-entity-mapping
```
Expected: All three commands found

**Step 3: Test Python imports**

```bash
python -c "from claimification import ClaimExtractionPipeline, EntityMappingPipeline"
python -c "from claimification.cli import main"
python -c "from claimification.mcp_servers.claim_extraction_server import main"
python -c "from claimification.mcp_servers.entity_mapping_server import main"
```
Expected: All imports succeed

**Step 4: Test CLI help**

```bash
claimification --help
```
Expected: Shows help message

**Step 5: Test MCP server can start (will need API key)**

```bash
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' | claimification-claim-extraction
```
Expected: JSON response or error about API key (proves server runs)

**Step 6: Run test suite**

```bash
pytest tests/ -v
```
Expected: All tests pass

**Step 7: Clean up test environment**

```bash
deactivate
rm -rf fresh_test_venv
```

**Step 8: Commit verification results**

```bash
git add .
git commit --allow-empty -m "test: final verification of v2.1.0 package structure"
```

---

## Task 18: Update Version and Create Tag

**Files:**
- Modify: `pyproject.toml` (version)
- Modify: `src/claimification/__init__.py` (version)
- Create: Git tag v2.1.0

**Step 1: Verify version in pyproject.toml**

Check line 7 in pyproject.toml:
```toml
version = "1.0.0"
```

Update to:
```toml
version = "2.1.0"
```

**Step 2: Verify version in __init__.py**

Already updated in Task 1 to `__version__ = "2.1.0"`

**Step 3: Commit version updates**

```bash
git add pyproject.toml
git commit -m "chore: bump version to 2.1.0"
```

**Step 4: Create git tag**

```bash
git tag -a v2.1.0 -m "Release v2.1.0 - Marketplace Ready Package"
```

**Step 5: Verify tag created**

Run: `git tag -l`
Expected: Shows v2.1.0 in list

**Step 6: Show tag details**

Run: `git show v2.1.0`
Expected: Shows tag annotation and commit

---

## Final Checklist

Before pushing to GitHub:

- [ ] All tests pass: `pytest tests/ -v`
- [ ] Package installs: `pip install .`
- [ ] Entry points work: `which claimification-claim-extraction`
- [ ] Imports work: `from claimification import *`
- [ ] Documentation updated
- [ ] Version bumped to 2.1.0
- [ ] Git tag created: v2.1.0
- [ ] No `from src.` imports remain (except backward compat)
- [ ] MCP servers start without Python path errors

## Push Commands

```bash
git push origin master
git push origin v2.1.0
```

---

## Success Criteria

✅ **Package Structure**
- `src/claimification/` namespace exists
- MCP servers in `src/claimification/mcp_servers/`
- All modules under `claimification.*`

✅ **Installation**
- `pip install .` succeeds
- Entry points installed as global commands
- No PYTHONPATH manipulation needed

✅ **Imports**
- `from claimification.claim_extraction import ClaimExtractionPipeline` works
- `from claimification.entity_mapping import EntityMappingPipeline` works
- Backward compatibility warnings shown for `from src.*`

✅ **MCP Servers**
- `claimification-claim-extraction` command available
- `claimification-entity-mapping` command available
- Servers can be configured in Claude Code with just command name

✅ **Documentation**
- README shows new import style
- Migration guide exists
- Release notes written

✅ **Testing**
- All tests pass
- Fresh install tested
- Entry points verified
