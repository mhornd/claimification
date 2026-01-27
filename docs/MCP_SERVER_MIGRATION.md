# Migration zu MCP-Server

**Datum:** 2026-01-27
**Status:** Design Phase
**Ziel:** Umbau von Skill-basiert zu MCP-Server-basiert für seamless Claude Code Integration

## Motivation

### Aktueller Zustand (Skill-basiert)
- Skill ist nur eine **Dokumentation/Anleitung** für Claude
- Claude muss manuell entscheiden, wie die Pipeline aufgerufen wird
- Typischerweise via `python -m src.main` über Bash-Tool
- User muss explizit warten, Claude muss Output parsen

### Gewünschter Zustand (MCP-Server)
- Pipeline wird als **direkt aufrufbares Tool** exponiert
- Claude sieht `mcp__claimification__extract_claims` Tool
- Tool-Aufruf → direktes Ergebnis (strukturiert)
- **Komplett automatisch:** User installiert einmal, Claude Code startet Server automatisch
- **Kein manueller Server-Start nötig**

## Recherche-Ergebnisse

### Offizielle Empfehlungen (Januar 2026)

**Quellen:**
- [MCP Official Specification](https://modelcontextprotocol.io/specification/2025-11-25)
- [Build an MCP Server Guide](https://modelcontextprotocol.io/docs/develop/build-server)
- [MCP Transport Comparison](https://mcpcat.io/guides/comparing-stdio-sse-streamablehttp/)
- [Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Claude Code MCP Docs](https://code.claude.com/docs/en/mcp)

**Transport-Wahl:**

| Transport | Use Case | Empfehlung für uns |
|-----------|----------|-------------------|
| **STDIO** | Lokale Tools, CLI-Integration | ✅ **JA** |
| Streamable HTTP | Cloud-Deployments, Browser | ❌ Nicht nötig |
| SSE (legacy) | Alte HTTP-basierte Systeme | ❌ Veraltet |

**Zitat aus offizieller Dokumentation:**
> "STDIO transport is ideal for local integrations and command-line tools. It's the simplest and most performant option for single-client scenarios."

**Für Claimification:** STDIO ist perfekt, da:
- Lokales Tool (keine Cloud nötig)
- Direkte Claude Code Integration
- User brauchen eigene API-Keys (OpenAI/Anthropic)
- Einfachste Implementierung

### Verfügbare Tools

1. **Official Python SDK** (`mcp` package)
   - Von Anthropic maintained
   - Abstrahiert JSON-RPC Protokoll
   - Type-safe Tool-Definitionen

2. **FastMCP** (High-level Framework)
   - Noch einfachere API als SDK
   - Speziell für schnelle Server-Entwicklung
   - Gute Claude Code Integration

**Empfehlung:** Official Python SDK nutzen (stabiler, offiziell supported)

## Gewählter Ansatz

### Ansatz: STDIO-basierter MCP-Server mit Official Python SDK

**Warum dieser Ansatz?**
- ✅ Offizielle Empfehlung für lokale Tools
- ✅ Kein Server-Setup nötig (läuft als Child-Prozess)
- ✅ Keine Ports/Netzwerk-Komplexität
- ✅ Official SDK macht Implementierung trivial
- ✅ Pipeline bleibt **komplett unverändert**
- ✅ TwoDigits Marketplace kompatibel

## Architektur

### Komponenten-Diagramm

```
┌─────────────────────────────────────────────────────────────┐
│                       Claude Code                           │
│                                                             │
│  - Startet mcp_server.py automatisch beim Launch           │
│  - Sieht Tool: mcp__claimification__extract_claims         │
│  - Kommuniziert via stdin/stdout                           │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ JSON-RPC über stdio
                     │
┌────────────────────▼────────────────────────────────────────┐
│                   mcp_server.py                             │
│                                                             │
│  - Nutzt Official Python SDK: from mcp.server import Server│
│  - Registriert Tool: "extract_claims"                      │
│  - Input: text (string), optional: question (string)       │
│  - Output: ClaimificationResult (JSON)                     │
│  - Läuft als Child-Prozess (kein manueller Start)          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ Function call
                     │
┌────────────────────▼────────────────────────────────────────┐
│            Bestehende Pipeline (UNVERÄNDERT)                │
│                                                             │
│  src/pipeline.py                                           │
│  ├─ ClaimificationPipeline                                 │
│  ├─ Stage 1: Sentence Splitting                            │
│  ├─ Stage 2: Selection                                     │
│  ├─ Stage 3: Disambiguation                                │
│  └─ Stage 4: Decomposition                                 │
│                                                             │
│  Alle LangChain Agents, Pydantic Models etc. bleiben       │
└─────────────────────────────────────────────────────────────┘
```

### User Experience Flow

**User macht einmal:**
```bash
claude mcp install twodigits/claimification
# Trägt API Key in .env ein (wird vom Installer erklärt)
```

**Dann automatisch:**
1. Claude Code startet beim Launch `python mcp_server.py`
2. MCP-Server läuft im Hintergrund als Child-Prozess
3. Claude sieht Tool `extract_claims` in der Toolbox

**User sagt:** "Extrahiere die Fakten aus diesem Text: ..."

**Claude macht:**
```python
# Tool call (automatisch)
result = mcp__claimification__extract_claims(text="...")
# Zeigt strukturiertes Ergebnis
```

**User sieht:** Sofort die extrahierten Claims, formatiert

## Implementierungsplan

### Neue Dateien

```
claimification/
├── mcp_server.py              # NEU: STDIO MCP-Server
├── src/
│   ├── mcp/                   # NEU: MCP-spezifische Adapter
│   │   ├── __init__.py
│   │   ├── tools.py           # Tool-Definitionen
│   │   └── handlers.py        # Request Handler
│   ├── pipeline.py            # UNVERÄNDERT
│   └── ...                    # ALLES UNVERÄNDERT
├── marketplace-metadata.json  # ANPASSEN: skills → mcpServers
└── docs/
    └── MCP_SERVER_MIGRATION.md  # Diese Datei
```

### Änderungen an bestehenden Dateien

**1. `marketplace-metadata.json`**

Vorher:
```json
{
  "skills": [
    {
      "name": "extract-claims",
      "description": "Extract verifiable factual claims from any text input",
      "usage": "/extract-claims"
    }
  ]
}
```

Nachher:
```json
{
  "mcpServers": {
    "claimification": {
      "command": "python",
      "args": ["mcp_server.py"],
      "env": {
        "OPENAI_API_KEY": "${OPENAI_API_KEY}",
        "ANTHROPIC_API_KEY": "${ANTHROPIC_API_KEY}"
      }
    }
  }
}
```

**2. `requirements.txt`**

Hinzufügen:
```
mcp>=1.0.0  # Official Python SDK
```

### Neue Implementierung: `mcp_server.py`

**Pseudo-Code:**

```python
from mcp.server import Server
from mcp.types import Tool, TextContent
from src.pipeline import ClaimificationPipeline

# Server initialisieren
server = Server("claimification")

# Tool registrieren
@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="extract_claims",
            description="Extract verifiable factual claims from text",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string"},
                    "question": {"type": "string", "optional": True}
                }
            }
        )
    ]

# Tool handler
@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "extract_claims":
        # Bestehende Pipeline aufrufen (UNVERÄNDERT)
        pipeline = ClaimificationPipeline()
        result = pipeline.extract_claims(
            text=arguments["text"],
            question=arguments.get("question")
        )

        # Result als JSON zurückgeben
        return [TextContent(
            type="text",
            text=format_result_as_markdown(result)
        )]

# STDIO-basierter Transport starten
if __name__ == "__main__":
    server.run()  # Läuft auf stdin/stdout
```

### Pipeline-Integration

**WICHTIG:** Die Pipeline bleibt **komplett unverändert**!

Der MCP-Server ist nur ein dünner Wrapper:
```python
# In mcp_server.py
from src.pipeline import ClaimificationPipeline  # Existing!
from src.models.result import ClaimificationResult  # Existing!

# Einfach aufrufen:
pipeline = ClaimificationPipeline(
    model=os.getenv("CLAIMIFICATION_MODEL", "gpt-5-nano-2025-08-07"),
    temperature=0.0
)
result: ClaimificationResult = pipeline.extract_claims(text=text)
```

**Kein Code in `src/` wird geändert!**

## TwoDigits Marketplace Integration

### Installation

**User führt aus:**
```bash
claude mcp install twodigits/claimification
```

**Was passiert:**
1. Marketplace lädt Repository
2. Führt `pip install -r requirements.txt` aus
3. Registriert MCP-Server in Claude Code Config
4. Zeigt User Info: "Bitte API-Key in .env eintragen"

### Konfiguration

Nach Installation erstellt User `.env`:
```bash
# Einer der beiden Keys ist required
OPENAI_API_KEY=sk-...
# ODER
ANTHROPIC_API_KEY=sk-ant-...

# Optional: Model override
CLAIMIFICATION_MODEL=gpt-5-nano-2025-08-07
```

**Wichtig:** User nutzt eigene API-Keys, kein TwoDigits Backend nötig!

### Backward Compatibility

**Skill wird entfernt** - MCP-Server ersetzt es komplett.

Warum?
- Skills waren nur Dokumentation
- MCP-Tools sind die "richtige" Integration
- Keine User verwenden aktuell das Skill (neu entwickelt)

## Sicherheit

### API-Keys

- User verwalten eigene Keys (in `.env`)
- Keys werden als Environment Variables übergeben
- Nie in Repository committed (`.env` in `.gitignore`)

### Input Validation

```python
def validate_input(text: str, question: str = None):
    if not text or len(text.strip()) == 0:
        raise ValueError("Text cannot be empty")
    if len(text) > 50000:  # ~50KB limit
        raise ValueError("Text too long (max 50,000 characters)")
    return True
```

### Error Handling

```python
try:
    result = pipeline.extract_claims(text=text)
    return format_success(result)
except Exception as e:
    return format_error(
        error=str(e),
        suggestion="Check your API key and input text"
    )
```

## Testing

### Manuelle Tests

**1. Installation testen:**
```bash
claude mcp install twodigits/claimification
# → Sollte ohne Fehler durchlaufen
```

**2. Server starten (manuell für Debug):**
```bash
python mcp_server.py
# → Sollte auf stdin warten
```

**3. Tool aufrufen in Claude Code:**
```
User: "Extrahiere Fakten aus: Der Himmel ist blau"
Claude: [Nutzt Tool automatisch]
→ Output: "1. Der Himmel ist blau."
```

### Automatische Tests

Bestehende Tests bleiben unverändert (Pipeline ist unverändert).

Neue Tests für MCP-Server:
```python
# tests/test_mcp_server.py
async def test_extract_claims_tool():
    result = await call_tool(
        name="extract_claims",
        arguments={"text": "Der Himmel ist blau"}
    )
    assert "Der Himmel ist blau" in result[0].text
```

## Roadmap

### Phase 1: Core Implementation (v1.1.0)
- [ ] Implementiere `mcp_server.py` mit Official Python SDK
- [ ] Update `marketplace-metadata.json` (skills → mcpServers)
- [ ] Füge `mcp` zu `requirements.txt` hinzu
- [ ] Teste Installation im TwoDigits Marketplace
- [ ] Teste Tool-Aufruf in Claude Code

### Phase 2: Polish (v1.1.1)
- [ ] Verbessere Error Messages
- [ ] Füge Input Validation hinzu
- [ ] Optimiere Output-Formatierung
- [ ] Schreibe MCP-Server Tests

### Phase 3: Documentation (v1.1.2)
- [ ] Update README.md (MCP statt Skill)
- [ ] Update INSTALLATION.md
- [ ] Füge MCP-Server Troubleshooting Guide hinzu
- [ ] Erstelle Video-Tutorial

### Phase 4: Advanced Features (v1.2.0)
- [ ] Batch processing tool (`extract_claims_batch`)
- [ ] Configuration tool (`configure_claimification`)
- [ ] Model selection per request
- [ ] Caching für wiederholte Claims

## Abhängigkeiten

### Python Packages (neu)
```
mcp>=1.0.0  # Official Python SDK
```

### Bestehende Dependencies (unverändert)
```
langchain>=0.1.0
langchain-openai>=0.0.5
langchain-anthropic>=0.1.0
pydantic>=2.0.0
python-dotenv>=1.0.0
rich>=13.0.0
```

## Kompatibilität

### Python Versions
- Minimum: Python 3.10
- Getestet: 3.10, 3.11, 3.12

### Platforms
- macOS ✅
- Linux ✅
- Windows ✅ (STDIO funktioniert überall)

### Claude Code Versions
- Minimum: v1.0.0 (mit MCP-Support)

## Migration für User

**Bestehende User (falls es welche gibt):**

Alt:
```bash
# Skill verwenden
/extract-claims [text]
```

Neu:
```bash
# Einfach installieren, dann automatisch
claude mcp install twodigits/claimification
# Tool wird automatisch von Claude erkannt
```

**Breaking Change:** Ja, aber kein Problem da:
- Plugin ist neu (v1.0.7 gerade released)
- Wahrscheinlich keine User noch
- Skill → MCP ist Standard-Migration Path

## Offene Fragen

1. **FastMCP vs Official SDK?**
   - Entscheidung: Official SDK (stabiler, langfristig supported)

2. **Output Format?**
   - Markdown (für gute Lesbarkeit in Claude Code)
   - Optional: JSON raw output?

3. **Error Handling Strategy?**
   - User-friendly messages
   - Suggestion for fixes
   - Never expose stack traces to Claude

4. **Backward compatibility mit CLI?**
   - Ja! `python -m src.main` funktioniert weiterhin
   - Nur Marketplace-Integration ändert sich

## Referenzen

- [MCP Official Specification](https://modelcontextprotocol.io/specification/2025-11-25)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Claude Code MCP Documentation](https://code.claude.com/docs/en/mcp)
- [MCP Transport Comparison](https://mcpcat.io/guides/comparing-stdio-sse-streamablehttp/)
- [Building MCP Servers Guide](https://modelcontextprotocol.io/docs/develop/build-server)

## Notizen

- Pipeline-Code bleibt **unverändert** ✅
- Kein externer Server nötig ✅
- User brauchen nur API-Keys ✅
- Seamless Claude Code Integration ✅
- TwoDigits Marketplace kompatibel ✅
