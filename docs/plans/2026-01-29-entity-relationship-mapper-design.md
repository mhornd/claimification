# Entity Relationship Mapper - Design Document

**Date:** 2026-01-29
**Status:** Approved
**Version:** 1.0

## Overview

The **Entity Relationship Mapper** is a new feature for the Claimification plugin that extracts entities and their relationships from unstructured text (e.g., LLM outputs) and produces both a programmatically queryable Knowledge Graph and a natural language summary.

### Core Value Proposition

- 📊 **Structure Chaos**: Transform unstructured LLM outputs into queryable knowledge structures
- 🔗 **Discover Hidden Connections**: Find implicit relationships through LLM-based inference
- 🎯 **Production-Ready**: Multi-stage pipeline architecture, fully testable

## Integration Strategy

- **Plugin Structure**: Extends Claimification plugin with a second parallel MCP server
- **Independence**: Entity mapping is independent from claim extraction (can be used separately)
- **Shared Plugin**: Both features live in the same `claimification` repository as separate MCP servers

## Input/Output Specification

### Input
- **Primary**: Unstructured text (any plain text)
- **Optional**: Contextual information (e.g., original question that prompted the text)

### Output Formats
1. **Knowledge Graph (JSON/NetworkX)**: Structured graph with nodes (entities) and edges (relationships)
2. **Natural Language Summary**: Human-readable text description of entities and relationships

### Example

**Input:**
```
Sarah Johnson founded TechCorp in 2020. The company, based in Berlin,
recently hired Marcus Lee as CTO. Lee previously worked at DataSystems.
```

**Output (JSON):**
```json
{
  "entities": [
    {"id": "e1", "text": "Sarah Johnson", "type": "PERSON"},
    {"id": "e2", "text": "TechCorp", "type": "ORGANIZATION"},
    {"id": "e3", "text": "Marcus Lee", "type": "PERSON"},
    {"id": "e4", "text": "DataSystems", "type": "ORGANIZATION"}
  ],
  "relationships": [
    {
      "source_entity_id": "e1",
      "target_entity_id": "e2",
      "relationship_type": "founded",
      "evidence": "Sarah Johnson founded TechCorp in 2020",
      "is_inferred": false,
      "confidence": 1.0
    },
    {
      "source_entity_id": "e3",
      "target_entity_id": "e2",
      "relationship_type": "works_at",
      "evidence": "hired as CTO",
      "is_inferred": true,
      "confidence": 0.95,
      "reasoning": "Being hired as CTO implies current employment"
    },
    {
      "source_entity_id": "e3",
      "target_entity_id": "e4",
      "relationship_type": "previously_worked_at",
      "evidence": "Lee previously worked at DataSystems",
      "is_inferred": false,
      "confidence": 1.0
    }
  ]
}
```

**Output (Natural Language Summary):**
```
The text describes 4 entities: Sarah Johnson (person), TechCorp (organization),
Marcus Lee (person), and DataSystems (organization).

Explicit relationships (2):
1. Sarah Johnson founded TechCorp
2. Marcus Lee previously worked at DataSystems

Inferred relationships (1):
1. Marcus Lee works at TechCorp (confidence: 0.95)
   → Inferred from: "hired as CTO" implies current employment
```

## Architecture

### Multi-Stage Pipeline

Following Claimification's proven architecture pattern, the Entity Relationship Mapper uses a **3-stage pipeline**:

#### Stage 1: Entity Extraction
**Responsibility:** Identify all relevant entities in the text

**Process:**
1. LLM extracts entities with type classification
2. Entity types: PERSON, ORGANIZATION, LOCATION, PRODUCT, EVENT, CONCEPT, DATE, OTHER
3. Coreference resolution: Map pronouns and aliases to canonical entity names
   - Example: "Sarah ... she ... the founder" → all resolve to "Sarah Johnson"
4. Deduplication: Merge variations of the same entity
   - Example: "TechCorp" and "TechCorp GmbH" → single entity

**Output:** List of normalized entities with unique IDs and types

#### Stage 2: Explicit Relationship Extraction
**Responsibility:** Extract directly stated relationships from the text

**Process:**
1. LLM analyzes sentences containing entities
2. Extracts relationship triples: (Entity1, Relationship-Type, Entity2)
3. Relationship types: founded, works_at, located_in, part_of, created, acquired, etc.
4. Each relationship annotated with source text span (evidence)

**Critical Constraint:** Only extract relationships that are **explicitly stated** in the text. No inference at this stage.

**Output:** List of explicit relationships with textual evidence

#### Stage 3: Relationship Inference
**Responsibility:** Infer implicit relationships using LLM reasoning

**Process:**
1. Identify entity pairs that co-occur but lack explicit relationships
2. LLM infers logical relationships based on context
3. Examples:
   - "hired as CTO" → infers "works_at"
   - "CEO of X" + "X acquired Y" → infers CEO has connection to Y
4. Each inference includes:
   - Confidence score (0.0 - 1.0)
   - Reasoning/justification

**Output:** List of inferred relationships with confidence scores and reasoning

### Data Models

All models use Pydantic for structured, type-safe outputs:

```python
# src/entity_mapping/models/entity.py
class EntityType(str, Enum):
    PERSON = "PERSON"
    ORGANIZATION = "ORGANIZATION"
    LOCATION = "LOCATION"
    PRODUCT = "PRODUCT"
    EVENT = "EVENT"
    CONCEPT = "CONCEPT"
    DATE = "DATE"
    OTHER = "OTHER"

class Entity(BaseModel):
    id: str                      # e.g., "e1", "e2"
    text: str                    # Canonical form: "Sarah Johnson"
    type: EntityType             # Entity classification
    mentions: List[str]          # All text spans: ["Sarah", "she", "the founder"]
    context: Optional[str]       # Surrounding sentence for disambiguation

# src/entity_mapping/models/relationship.py
class Relationship(BaseModel):
    source_entity_id: str        # References Entity.id
    target_entity_id: str        # References Entity.id
    relationship_type: str       # "founded", "works_at", etc.
    evidence: str                # Text span supporting this relationship
    is_inferred: bool            # False = explicit, True = inferred
    confidence: float = 1.0      # 1.0 for explicit, <1.0 for inferred
    reasoning: Optional[str]     # Explanation (only for inferred)

# src/entity_mapping/models/knowledge_graph.py
class KnowledgeGraph(BaseModel):
    entities: List[Entity]
    relationships: List[Relationship]
    metadata: GraphMetadata

    def to_networkx(self) -> nx.DiGraph:
        """Convert to NetworkX graph for programmatic analysis"""

    def to_summary(self) -> str:
        """Generate natural language summary"""

    def to_json(self) -> dict:
        """Export as JSON"""
```

## Repository Structure

Updated repository layout to accommodate both features:

```
claimification/
├── src/
│   ├── claim_extraction/          # Existing: Claim extraction pipeline
│   │   ├── stages/
│   │   ├── models/
│   │   ├── prompts/
│   │   └── pipeline.py
│   │
│   └── entity_mapping/            # NEW: Entity relationship pipeline
│       ├── __init__.py
│       ├── pipeline.py            # EntityMappingPipeline class
│       ├── stages/
│       │   ├── __init__.py
│       │   ├── entity_extraction.py
│       │   ├── relationship_extraction.py
│       │   └── relationship_inference.py
│       ├── models/
│       │   ├── __init__.py
│       │   ├── entity.py
│       │   ├── relationship.py
│       │   └── knowledge_graph.py
│       ├── prompts/
│       │   ├── __init__.py
│       │   ├── entity_extraction.py
│       │   ├── relationship_extraction.py
│       │   └── relationship_inference.py
│       └── utils/
│           ├── __init__.py
│           └── graph_utils.py     # NetworkX helpers, visualization
│
├── mcp_servers/                   # NEW: Multiple MCP servers
│   ├── claim_extraction_server.py # Moved from root mcp_server.py
│   └── entity_mapping_server.py   # NEW: Entity mapping MCP server
│
├── .claude-plugin/
│   └── plugin.json                # Updated with 2 MCP servers
│
├── tests/
│   ├── claim_extraction/          # Existing tests
│   └── entity_mapping/            # NEW: Entity mapping tests (future)
│
└── docs/
    ├── claim_extraction/          # Existing docs
    ├── entity_mapping/            # NEW: Entity mapping docs
    └── plans/
        └── 2026-01-29-entity-relationship-mapper-design.md  # This document
```

## MCP Server Configuration

Updated `plugin.json` to expose both features:

```json
{
  "name": "claimification",
  "version": "2.0.0",
  "description": "Extract claims and map entity relationships from any text",
  "mcpServers": {
    "claim-extraction": {
      "command": "python",
      "args": ["mcp_servers/claim_extraction_server.py"],
      "env": {
        "OPENAI_API_KEY": "${OPENAI_API_KEY}",
        "ANTHROPIC_API_KEY": "${ANTHROPIC_API_KEY}"
      }
    },
    "entity-mapping": {
      "command": "python",
      "args": ["mcp_servers/entity_mapping_server.py"],
      "env": {
        "OPENAI_API_KEY": "${OPENAI_API_KEY}",
        "ANTHROPIC_API_KEY": "${ANTHROPIC_API_KEY}"
      }
    }
  }
}
```

### MCP Tools Exposed

The `entity-mapping` MCP server will expose:

```python
@server.call_tool()
async def extract_entities_and_relationships(
    text: str,
    context: Optional[str] = None,
    include_inferred: bool = True,
    confidence_threshold: float = 0.7
) -> KnowledgeGraph:
    """
    Extract entities and relationships from text.

    Args:
        text: The unstructured text to analyze
        context: Optional contextual information (e.g., original question)
        include_inferred: Whether to include inferred relationships
        confidence_threshold: Minimum confidence for inferred relationships

    Returns:
        Complete knowledge graph with entities and relationships
    """

@server.call_tool()
async def visualize_graph(
    knowledge_graph: KnowledgeGraph,
    format: str = "mermaid"  # or "graphviz"
) -> str:
    """
    Generate visualization of the knowledge graph.

    Args:
        knowledge_graph: The graph to visualize
        format: Output format (mermaid, graphviz)

    Returns:
        Visualization markup/code
    """
```

## Prompt Design Principles

### Stage 1: Entity Extraction
**Focus:** Precision in entity identification and coreference resolution

```python
SYSTEM_PROMPT = """You are an expert at identifying and extracting named entities from text.

Extract ALL entities and resolve coreferences (pronouns, abbreviations, aliases).

Rules:
- Use canonical forms (full names, not abbreviations)
- Classify entity types accurately
- Track all mentions of each entity
- Be conservative - only extract clearly identifiable entities
"""
```

### Stage 2: Relationship Extraction
**Focus:** Extract only explicit relationships with clear textual evidence

```python
SYSTEM_PROMPT = """You extract relationships that are EXPLICITLY stated in the text.

Rules:
- Every relationship must have direct textual evidence
- Do NOT infer or guess relationships
- If a relationship is ambiguous, skip it (Stage 3 handles inference)
- Provide the exact text span that states the relationship
"""
```

### Stage 3: Relationship Inference
**Focus:** Conservative inference with justification

```python
SYSTEM_PROMPT = """You infer implicit relationships using logical reasoning.

Rules:
- Only infer relationships with high confidence (>0.7)
- Always provide reasoning/justification
- Conservative approach: when uncertain, don't infer
- Consider context and common-sense knowledge
"""
```

## Implementation Phases

### Phase 1: Repository Restructuring
1. Create new directory structure (`src/entity_mapping/`, `mcp_servers/`)
2. Move existing `mcp_server.py` → `mcp_servers/claim_extraction_server.py`
3. Update `plugin.json` with dual MCP server configuration
4. Update imports in claim extraction code

### Phase 2: Data Models
1. Implement `Entity`, `EntityType`, `Relationship` models
2. Implement `KnowledgeGraph` with export methods:
   - `to_json()`
   - `to_networkx()`
   - `to_summary()`
3. Add NetworkX integration for graph analysis

### Phase 3: Stage 1 - Entity Extraction
1. Design and iterate on prompt
2. Implement LangChain agent
3. Handle coreference resolution
4. Handle entity deduplication

### Phase 4: Stage 2 - Explicit Relationship Extraction
1. Design prompt (focus: evidence tracking)
2. Implement LangChain agent
3. Ensure no inference happens

### Phase 5: Stage 3 - Relationship Inference
1. Design prompt (focus: reasoning + confidence)
2. Implement LangChain agent
3. Implement confidence thresholding

### Phase 6: Pipeline Integration
1. Create `EntityMappingPipeline` class
2. Orchestrate 3 stages
3. Handle errors and retries

### Phase 7: MCP Server
1. Implement `entity_mapping_server.py`
2. Expose tools
3. Test integration with Claude Code

### Phase 8: Documentation
1. Write usage guide
2. Write API reference
3. Update main README

## Design Decisions

### Why 3 Stages Instead of Single-Pass?
- **Modularity**: Each stage has clear responsibility, easier to debug
- **Testability**: Can test each stage independently
- **Quality**: Separation of explicit vs. inferred improves accuracy
- **Follows Proven Pattern**: Mirrors successful Claimification architecture

### Why LLM Inference vs. Co-Occurrence Only?
- **Richer Relationships**: Co-occurrence only captures "mentioned together"
- **Semantic Understanding**: LLMs can infer "works_at" from "hired as CTO"
- **Confidence Scores**: LLM can quantify certainty of inference
- **Reasoning**: Provides explanations, improving trust and debuggability

### Why No src/shared/ Yet?
- **Avoid Premature Abstraction**: Unclear what will truly be shared
- **Iterate First**: Build both pipelines, then extract commonalities
- **Simplicity**: Less cognitive overhead during initial development

### Why NetworkX + JSON?
- **NetworkX**: Industry-standard graph library, enables graph algorithms
- **JSON**: Universal format, easy integration with other tools
- **Both**: NetworkX for analysis, JSON for storage/transfer

## Success Criteria

A successful implementation will:

1. ✅ Extract entities with >90% accuracy on diverse texts
2. ✅ Resolve coreferences correctly (pronouns → canonical names)
3. ✅ Extract explicit relationships with textual evidence
4. ✅ Infer implicit relationships with confidence scores
5. ✅ Export valid NetworkX graphs
6. ✅ Generate readable natural language summaries
7. ✅ Function as independent MCP server alongside claim-extraction

## Future Enhancements (Out of Scope)

- Visualization UI (beyond text-based Mermaid/GraphViz)
- Multi-document relationship tracking
- Entity disambiguation against knowledge bases (Wikidata, etc.)
- Custom entity type definitions
- Relationship type ontologies
- Temporal relationship tracking (when relationships change)

## References

- Claimification claim extraction pipeline (existing architecture)
- NetworkX documentation: https://networkx.org/
- LangChain structured output: https://python.langchain.com/docs/modules/model_io/output_parsers/

---

**Design Approved:** 2026-01-29
**Next Steps:** Implementation planning and git worktree setup
