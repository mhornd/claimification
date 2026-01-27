# Claimification - Quick Start Guide

Willkommen bei Claimification! Dieses Repository enthält ein vollständig implementiertes Claude Code Plugin für die Extraktion von verifizierbaren Claims aus LLM-generierten Antworten.

## Was wurde erstellt?

Das Repository enthält jetzt:

✅ **Vollständige LangChain-Pipeline** mit 4 Stages
✅ **Claude Code Plugin** mit Skill-Integration
✅ **CLI-Interface** für Kommandozeilen-Nutzung
✅ **Python API** für programmatische Integration
✅ **Umfassende Dokumentation** (README, Installation, Usage)
✅ **Beispiele** für verschiedene Nutzungsszenarien

## Projektstruktur

```
claimification/
├── .claude-plugin/
│   └── plugin.json              ✅ Claude Code Plugin Manifest
├── src/
│   ├── stages/
│   │   ├── sentence_splitter.py     ✅ Stage 1: Satz-Splitting
│   │   ├── selection_agent.py       ✅ Stage 2: Verifiable Content
│   │   ├── disambiguation_agent.py  ✅ Stage 3: Ambiguität auflösen
│   │   └── decomposition_agent.py   ✅ Stage 4: Claim Extraction
│   ├── models/
│   │   ├── sentence.py          ✅ Sentence Datenmodelle
│   │   ├── claim.py             ✅ Claim Datenmodelle
│   │   └── result.py            ✅ Result Datenmodelle
│   ├── prompts/
│   │   ├── selection.py         ✅ Selection Prompts
│   │   ├── disambiguation.py    ✅ Disambiguation Prompts
│   │   └── decomposition.py     ✅ Decomposition Prompts
│   ├── pipeline.py              ✅ Pipeline Orchestrator
│   └── main.py                  ✅ CLI Entry Point
├── skills/
│   └── extract-claims           ✅ Claude Code Skill
├── examples/
│   └── basic_usage.py           ✅ Python API Beispiel
├── docs/
│   ├── INSTALLATION.md          ✅ Installation Guide
│   └── USAGE.md                 ✅ Usage Guide
├── requirements.txt             ✅ Dependencies
├── .env.example                 ✅ Environment Template
├── README.md                    ✅ Hauptdokumentation
└── LICENSE                      ✅ MIT License
```

## Nächste Schritte

### 1. Installation

```bash
# Dependencies installieren
pip install -r requirements.txt

# Environment konfigurieren
cp .env.example .env
# Füge deinen API Key zu .env hinzu:
# OPENAI_API_KEY=sk-... oder ANTHROPIC_API_KEY=sk-ant-...
```

### 2. Testen

```bash
# Beispiel ausführen
python examples/basic_usage.py
```

### 3. Claude Code Integration (Optional)

```bash
# Als Plugin in Claude Code installieren
/plugin install .
```

## Verwendung

### Python API

```python
from src import ClaimificationPipeline

pipeline = ClaimificationPipeline(model="gpt-4o")
result = pipeline.extract_claims(
    question="What are challenges in Argentina?",
    answer="Argentina's inflation rate reached 25.5%..."
)

for claim in result.get_all_claims():
    print(f"- {claim.text}")
```

### CLI

```bash
python -m src.main \
    --question "Your question" \
    --answer "Your answer" \
    --format markdown
```

### Claude Code Skill

```bash
/extract-claims
```

## Pipeline-Flow

```
Question + Answer
    ↓
┌─────────────────────────┐
│ Stage 1: Split Sentences │
└─────────────────────────┘
    ↓
┌─────────────────────────┐
│ Stage 2: Selection       │  ← LangChain Agent (GPT-4o/Claude)
│ (Verifiable Content?)    │
└─────────────────────────┘
    ↓
┌─────────────────────────┐
│ Stage 3: Disambiguation  │  ← LangChain Agent (GPT-4o/Claude)
│ (Resolve Ambiguity?)     │
└─────────────────────────┘
    ↓
┌─────────────────────────┐
│ Stage 4: Decomposition   │  ← LangChain Agent (GPT-4o/Claude)
│ (Extract Claims)         │
└─────────────────────────┘
    ↓
Extracted Claims (JSON/Markdown)
```

## Technologie-Stack

- **LangChain**: Agent-Orchestrierung mit strukturiertem Output
- **Pydantic**: Type-safe Datenmodelle
- **Rich**: Schöne CLI-Ausgabe mit Progress Bars
- **OpenAI/Anthropic**: LLM Provider
- **Python 3.10+**: Moderne Python Features

## Konfiguration

Alle Einstellungen können über Environment-Variablen gesteuert werden:

```bash
# Model
CLAIMIFICATION_MODEL=gpt-4o  # oder claude-3-5-sonnet-20241022

# Context
CLAIMIFICATION_CONTEXT_SENTENCES=2

# Temperature (für Determinismus)
CLAIMIFICATION_TEMPERATURE=0.0
```

## Beispiel Output

**Input:**
- Question: "What are challenges in Argentina?"
- Answer: "Argentina's inflation, reaching 25.5%, caused hardship."

**Output:**
```
A. Argentina's inflation, reaching 25.5%, caused hardship.

1. Argentina has inflation.
2. Argentina's inflation reached 25.5%.
3. Inflation caused hardship in Argentina.
```

## Nächste Entwicklungsschritte

Wenn du das Projekt weiterentwickeln möchtest:

1. **Tests hinzufügen**: Erstelle `tests/test_pipeline.py` mit pytest
2. **Marketplace Integration**: Bereite für TwoDigits Marketplace vor
3. **Performance**: Implementiere Batch-Processing für parallele Verarbeitung
4. **Caching**: Füge Caching für wiederholte Claims hinzu
5. **UI**: Erstelle eine Web-UI mit Streamlit oder Gradio

## Support & Ressourcen

- **README**: [README.md](README.md) - Komplette Dokumentation
- **Installation**: [docs/INSTALLATION.md](docs/INSTALLATION.md)
- **Usage**: [docs/USAGE.md](docs/USAGE.md)
- **Project Structure**: [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)
- **Research Paper**: [explanation.md](explanation.md)

## TwoDigits Marketplace

Dieses Plugin ist bereit für die Integration in den TwoDigits Marketplace:

1. Repository auf GitHub veröffentlichen
2. Metadata-File für Registry erstellen
3. PR im twodigits-marketplace Repository erstellen

Details im [README_of_marketplace_claude_code.md](README_of_marketplace_claude_code.md).

## Lizenz

MIT License - Siehe [LICENSE](LICENSE)

---

**Viel Erfolg mit Claimification! 🚀**

Bei Fragen oder Problemen kannst du Issues im GitHub Repository erstellen.
