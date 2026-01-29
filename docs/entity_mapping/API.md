# Entity Relationship Mapping - API Reference

## EntityMappingPipeline

Main pipeline class orchestrating all stages.

### Constructor

```python
EntityMappingPipeline(
    model: str = "gpt-5-nano-2025-08-07",
    temperature: float = 0.0,
    confidence_threshold: float = 0.7,
    include_inferred: bool = True
)
```

**Parameters:**
- `model` - LLM model to use (OpenAI or Anthropic)
- `temperature` - Sampling temperature (0.0 = deterministic)
- `confidence_threshold` - Minimum confidence for inferred relationships
- `include_inferred` - Whether to run Stage 3 (inference)

### Methods

#### extract_knowledge_graph

```python
def extract_knowledge_graph(
    text: str,
    context: Optional[str] = None
) -> KnowledgeGraph
```

Extract complete knowledge graph from text.

**Parameters:**
- `text` - The text to analyze
- `context` - Optional contextual information

**Returns:** `KnowledgeGraph` object

## Data Models

### Entity

```python
class Entity(BaseModel):
    id: str                    # Unique ID (e.g., "e1")
    text: str                  # Canonical name
    type: EntityType           # Entity classification
    mentions: List[str]        # All text references
    context: Optional[str]     # Disambiguation context
```

### Relationship

```python
class Relationship(BaseModel):
    source_entity_id: str      # Source entity ID
    target_entity_id: str      # Target entity ID
    relationship_type: str     # Relationship type
    evidence: str              # Supporting text
    is_inferred: bool          # Explicit vs inferred
    confidence: float          # 0.0-1.0
    reasoning: Optional[str]   # Inference explanation
```

### KnowledgeGraph

```python
class KnowledgeGraph(BaseModel):
    entities: List[Entity]
    relationships: List[Relationship]
    metadata: GraphMetadata

    def to_json() -> Dict[str, Any]
    def to_summary() -> str
```

## MCP Server Tool

### extract_entities_and_relationships

**Input Schema:**
```json
{
  "text": "string (required)",
  "context": "string (optional)",
  "model": "string (optional, default: gpt-5-nano-2025-08-07)",
  "include_inferred": "boolean (optional, default: true)",
  "confidence_threshold": "number (optional, default: 0.7)"
}
```

**Output:** Markdown-formatted text with:
1. Natural language summary
2. Metadata
3. JSON export

## Stage Classes

### EntityExtractionStage

```python
class EntityExtractionStage:
    def extract_entities(
        text: str,
        context: Optional[str] = None
    ) -> List[Entity]
```

### RelationshipExtractionStage

```python
class RelationshipExtractionStage:
    def extract_relationships(
        text: str,
        entities: List[Entity]
    ) -> List[Relationship]
```

### RelationshipInferenceStage

```python
class RelationshipInferenceStage:
    def infer_relationships(
        text: str,
        entities: List[Entity],
        existing_relationships: List[Relationship]
    ) -> List[Relationship]
```
