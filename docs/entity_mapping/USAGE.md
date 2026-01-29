# Entity Relationship Mapping - Usage Guide

## Overview

The Entity Relationship Mapper extracts entities and their relationships from unstructured text, producing both structured knowledge graphs and natural language summaries.

## Quick Start

### Via MCP Server (Claude Code)

The entity mapping MCP server is automatically available when you install the Claimification plugin.

```python
# In Claude Code, use the MCP tool
extract_entities_and_relationships(
    text="Sarah Johnson founded TechCorp in 2020. The company, based in Berlin, recently hired Marcus Lee as CTO.",
    include_inferred=True,
    confidence_threshold=0.7
)
```

### Programmatic Usage

```python
from src.entity_mapping import EntityMappingPipeline

# Initialize pipeline
pipeline = EntityMappingPipeline(
    model="gpt-5-nano-2025-08-07",
    temperature=0.0,
    confidence_threshold=0.7,
    include_inferred=True
)

# Extract knowledge graph
knowledge_graph = pipeline.extract_knowledge_graph(
    text="Sarah Johnson founded TechCorp in 2020...",
    context="Background on tech startups in Berlin"
)

# Access results
print(knowledge_graph.to_summary())  # Natural language
graph_json = knowledge_graph.to_json()  # JSON export
```

## Pipeline Stages

### Stage 1: Entity Extraction

Identifies and normalizes entities with coreference resolution.

**Entity Types:**
- PERSON
- ORGANIZATION
- LOCATION
- PRODUCT
- EVENT
- CONCEPT
- DATE
- OTHER

**Example:**
```
Input: "Sarah founded TechCorp. She is based in Berlin."
Output:
- Entity e1: "Sarah Johnson" (PERSON)
  Mentions: ["Sarah", "She"]
- Entity e2: "TechCorp" (ORGANIZATION)
- Entity e3: "Berlin" (LOCATION)
```

### Stage 2: Explicit Relationship Extraction

Extracts only relationships directly stated in the text.

**Common Relationship Types:**
- founded
- works_at
- located_in
- part_of
- acquired
- created

**Example:**
```
Input: "Sarah Johnson founded TechCorp"
Output:
- Relationship: e1 --founded--> e2
  Evidence: "Sarah Johnson founded TechCorp"
  Confidence: 1.0 (explicit)
```

### Stage 3: Relationship Inference

Infers implicit relationships using LLM reasoning.

**Example:**
```
Input: "hired Marcus Lee as CTO"
Output:
- Relationship: e3 --works_at--> e2
  Evidence: "hired as CTO"
  Confidence: 0.95
  Reasoning: "Being hired as CTO implies current employment"
```

## Configuration Options

### Model Selection

```python
pipeline = EntityMappingPipeline(model="gpt-5-nano-2025-08-07")
# or
pipeline = EntityMappingPipeline(model="claude-3-5-sonnet-20241022")
```

### Confidence Threshold

```python
# Only include inferences with confidence > 0.8
pipeline = EntityMappingPipeline(confidence_threshold=0.8)
```

### Disable Inference

```python
# Only extract explicit relationships
pipeline = EntityMappingPipeline(include_inferred=False)
```

## Output Formats

### Natural Language Summary

```python
summary = knowledge_graph.to_summary()
```

Output:
```
The text describes 3 entities:
- Sarah Johnson (PERSON)
- TechCorp (ORGANIZATION)
- Berlin (LOCATION)

Explicit relationships (1):
1. Sarah Johnson founded TechCorp

Inferred relationships (0):
(none)
```

### JSON Export

```python
json_data = knowledge_graph.to_json()
```

## Best Practices

1. **Provide Context**: Use the `context` parameter for better disambiguation
2. **Adjust Confidence Threshold**: Higher threshold = fewer but more certain inferences
3. **Review Inferences**: Always check reasoning for inferred relationships
4. **Use Appropriate Models**: gpt-5-nano for speed, claude for quality

## Limitations

- Maximum text length: 50,000 characters
- Entity extraction quality depends on text clarity
- Inference quality depends on LLM capabilities
- No support for multi-document analysis (yet)
