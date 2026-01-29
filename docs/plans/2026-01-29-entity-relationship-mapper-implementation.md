# Entity Relationship Mapper Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a 3-stage pipeline that extracts entities and relationships from unstructured text, outputting both structured knowledge graphs (JSON) and natural language summaries.

**Architecture:** Multi-stage LangChain pipeline (Entity Extraction → Explicit Relationships → Inferred Relationships), following proven Claimification pattern. Separate MCP server for entity mapping alongside existing claim extraction.

**Tech Stack:** Python 3.10+, LangChain, Pydantic, OpenAI/Anthropic APIs, MCP SDK

---

## Task 1: Repository Restructuring

**Goal:** Reorganize repository to support dual MCP servers

**Files:**
- Create: `mcp_servers/` directory
- Move: `mcp_server.py` → `mcp_servers/claim_extraction_server.py`
- Modify: `.claude-plugin/plugin.json`
- Create: `src/entity_mapping/` directory structure

### Step 1: Create mcp_servers directory and move existing server

```bash
mkdir -p mcp_servers
git mv mcp_server.py mcp_servers/claim_extraction_server.py
```

### Step 2: Update plugin.json for dual MCP servers

File: `.claude-plugin/plugin.json`

```json
{
  "name": "claimification",
  "version": "2.0.0",
  "description": "Extract claims and map entity relationships from any text",
  "author": {
    "name": "Marlo Horndasch",
    "email": "private",
    "url": "https://github.com/mhornd"
  },
  "license": "MIT",
  "repository": "https://github.com/mhornd/claimification",
  "homepage": "https://github.com/mhornd/claimification#readme",
  "keywords": [
    "fact-checking",
    "claim-extraction",
    "verification",
    "llm",
    "langchain",
    "ai-safety",
    "entity-extraction",
    "knowledge-graph",
    "relationship-mapping"
  ],
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

### Step 3: Create entity_mapping directory structure

```bash
mkdir -p src/entity_mapping/{models,stages,prompts,utils}
touch src/entity_mapping/__init__.py
touch src/entity_mapping/models/__init__.py
touch src/entity_mapping/stages/__init__.py
touch src/entity_mapping/prompts/__init__.py
touch src/entity_mapping/utils/__init__.py
```

### Step 4: Commit restructuring

```bash
git add -A
git commit -m "refactor: restructure for dual MCP servers

- Move mcp_server.py to mcp_servers/claim_extraction_server.py
- Update plugin.json to support both claim-extraction and entity-mapping
- Create src/entity_mapping/ directory structure
- Bump version to 2.0.0

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## Task 2: Data Models - Entity

**Goal:** Create Entity and EntityType models with Pydantic

**Files:**
- Create: `src/entity_mapping/models/entity.py`
- Modify: `src/entity_mapping/models/__init__.py`

### Step 1: Implement EntityType enum and Entity model

File: `src/entity_mapping/models/entity.py`

```python
"""Entity data models for entity relationship mapping."""

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class EntityType(str, Enum):
    """Types of entities that can be extracted."""

    PERSON = "PERSON"
    ORGANIZATION = "ORGANIZATION"
    LOCATION = "LOCATION"
    PRODUCT = "PRODUCT"
    EVENT = "EVENT"
    CONCEPT = "CONCEPT"
    DATE = "DATE"
    OTHER = "OTHER"


class Entity(BaseModel):
    """Represents an extracted entity with metadata.

    An entity is a canonical representation of a real-world object
    mentioned in the text, with all its textual mentions tracked.
    """

    id: str = Field(
        ...,
        description="Unique identifier (e.g., 'e1', 'e2')"
    )

    text: str = Field(
        ...,
        description="Canonical form of the entity (e.g., 'Sarah Johnson')"
    )

    type: EntityType = Field(
        ...,
        description="Classification of the entity"
    )

    mentions: List[str] = Field(
        default_factory=list,
        description="All text spans referring to this entity (e.g., ['Sarah', 'she', 'the founder'])"
    )

    context: Optional[str] = Field(
        default=None,
        description="Surrounding sentence for disambiguation"
    )

    class Config:
        """Pydantic config."""
        use_enum_values = True
```

### Step 2: Export models from __init__.py

File: `src/entity_mapping/models/__init__.py`

```python
"""Data models for entity relationship mapping."""

from src.entity_mapping.models.entity import Entity, EntityType

__all__ = ["Entity", "EntityType"]
```

### Step 3: Commit entity models

```bash
git add src/entity_mapping/models/entity.py src/entity_mapping/models/__init__.py
git commit -m "feat: add Entity and EntityType models

- Create EntityType enum with 8 entity categories
- Create Entity model with id, text, type, mentions, context
- Use Pydantic for structured validation

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## Task 3: Data Models - Relationship

**Goal:** Create Relationship model with support for explicit and inferred relationships

**Files:**
- Create: `src/entity_mapping/models/relationship.py`
- Modify: `src/entity_mapping/models/__init__.py`

### Step 1: Implement Relationship model

File: `src/entity_mapping/models/relationship.py`

```python
"""Relationship data models for entity relationship mapping."""

from typing import Optional
from pydantic import BaseModel, Field, field_validator


class Relationship(BaseModel):
    """Represents a relationship between two entities.

    Relationships can be explicit (directly stated in text) or
    inferred (derived through LLM reasoning).
    """

    source_entity_id: str = Field(
        ...,
        description="ID of the source entity"
    )

    target_entity_id: str = Field(
        ...,
        description="ID of the target entity"
    )

    relationship_type: str = Field(
        ...,
        description="Type of relationship (e.g., 'founded', 'works_at', 'located_in')"
    )

    evidence: str = Field(
        ...,
        description="Text span supporting this relationship"
    )

    is_inferred: bool = Field(
        default=False,
        description="False for explicit relationships, True for inferred"
    )

    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Confidence score (1.0 for explicit, <1.0 for inferred)"
    )

    reasoning: Optional[str] = Field(
        default=None,
        description="Explanation for inferred relationships"
    )

    @field_validator('confidence')
    @classmethod
    def validate_confidence(cls, v: float, info) -> float:
        """Ensure explicit relationships have confidence 1.0."""
        is_inferred = info.data.get('is_inferred', False)
        if not is_inferred and v != 1.0:
            raise ValueError("Explicit relationships must have confidence 1.0")
        return v

    @field_validator('reasoning')
    @classmethod
    def validate_reasoning(cls, v: Optional[str], info) -> Optional[str]:
        """Ensure inferred relationships have reasoning."""
        is_inferred = info.data.get('is_inferred', False)
        if is_inferred and not v:
            raise ValueError("Inferred relationships must include reasoning")
        return v
```

### Step 2: Update __init__.py

File: `src/entity_mapping/models/__init__.py`

```python
"""Data models for entity relationship mapping."""

from src.entity_mapping.models.entity import Entity, EntityType
from src.entity_mapping.models.relationship import Relationship

__all__ = ["Entity", "EntityType", "Relationship"]
```

### Step 3: Commit relationship model

```bash
git add src/entity_mapping/models/relationship.py src/entity_mapping/models/__init__.py
git commit -m "feat: add Relationship model

- Create Relationship model with source/target entity IDs
- Support both explicit and inferred relationships
- Add confidence scores and reasoning for inferred relationships
- Validate that explicit relationships have confidence=1.0

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## Task 4: Data Models - Knowledge Graph

**Goal:** Create KnowledgeGraph model with export methods (JSON, summary)

**Files:**
- Create: `src/entity_mapping/models/knowledge_graph.py`
- Modify: `src/entity_mapping/models/__init__.py`

### Step 1: Implement KnowledgeGraph model

File: `src/entity_mapping/models/knowledge_graph.py`

```python
"""Knowledge graph data model."""

from typing import List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

from src.entity_mapping.models.entity import Entity
from src.entity_mapping.models.relationship import Relationship


class GraphMetadata(BaseModel):
    """Metadata about graph generation."""

    created_at: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat(),
        description="ISO timestamp of graph creation"
    )

    model_used: str = Field(
        ...,
        description="LLM model used for extraction"
    )

    total_entities: int = Field(
        ...,
        description="Total number of entities extracted"
    )

    total_relationships: int = Field(
        ...,
        description="Total number of relationships extracted"
    )

    explicit_relationships: int = Field(
        ...,
        description="Number of explicit relationships"
    )

    inferred_relationships: int = Field(
        ...,
        description="Number of inferred relationships"
    )


class KnowledgeGraph(BaseModel):
    """Represents a complete knowledge graph extracted from text.

    Contains entities, relationships, and methods to export in
    various formats (JSON, natural language summary).
    """

    entities: List[Entity] = Field(
        default_factory=list,
        description="List of extracted entities"
    )

    relationships: List[Relationship] = Field(
        default_factory=list,
        description="List of relationships between entities"
    )

    metadata: GraphMetadata = Field(
        ...,
        description="Metadata about graph generation"
    )

    def to_json(self) -> Dict[str, Any]:
        """Export as JSON dictionary.

        Returns:
            Dictionary representation of the knowledge graph
        """
        return {
            "entities": [entity.model_dump() for entity in self.entities],
            "relationships": [rel.model_dump() for rel in self.relationships],
            "metadata": self.metadata.model_dump()
        }

    def to_summary(self) -> str:
        """Generate natural language summary of the knowledge graph.

        Returns:
            Human-readable text description
        """
        lines = []

        # Entity summary
        entity_count = len(self.entities)
        if entity_count == 0:
            lines.append("The text contains no identifiable entities.")
            return "\n".join(lines)

        lines.append(f"The text describes {entity_count} entities:")
        for entity in self.entities:
            lines.append(f"- {entity.text} ({entity.type})")
        lines.append("")

        # Relationship summary
        explicit_rels = [r for r in self.relationships if not r.is_inferred]
        inferred_rels = [r for r in self.relationships if r.is_inferred]

        if explicit_rels:
            lines.append(f"Explicit relationships ({len(explicit_rels)}):")
            for i, rel in enumerate(explicit_rels, 1):
                source = self._get_entity_text(rel.source_entity_id)
                target = self._get_entity_text(rel.target_entity_id)
                lines.append(f"{i}. {source} {rel.relationship_type} {target}")
            lines.append("")

        if inferred_rels:
            lines.append(f"Inferred relationships ({len(inferred_rels)}):")
            for i, rel in enumerate(inferred_rels, 1):
                source = self._get_entity_text(rel.source_entity_id)
                target = self._get_entity_text(rel.target_entity_id)
                lines.append(
                    f"{i}. {source} {rel.relationship_type} {target} "
                    f"(confidence: {rel.confidence:.2f})"
                )
                lines.append(f"   → {rel.reasoning}")
            lines.append("")

        if not explicit_rels and not inferred_rels:
            lines.append("No relationships identified between entities.")

        return "\n".join(lines)

    def _get_entity_text(self, entity_id: str) -> str:
        """Helper to get entity text by ID.

        Args:
            entity_id: Entity ID to look up

        Returns:
            Entity canonical text, or ID if not found
        """
        for entity in self.entities:
            if entity.id == entity_id:
                return entity.text
        return entity_id  # Fallback
```

### Step 2: Update __init__.py

File: `src/entity_mapping/models/__init__.py`

```python
"""Data models for entity relationship mapping."""

from src.entity_mapping.models.entity import Entity, EntityType
from src.entity_mapping.models.relationship import Relationship
from src.entity_mapping.models.knowledge_graph import (
    KnowledgeGraph,
    GraphMetadata
)

__all__ = [
    "Entity",
    "EntityType",
    "Relationship",
    "KnowledgeGraph",
    "GraphMetadata"
]
```

### Step 3: Commit knowledge graph model

```bash
git add src/entity_mapping/models/knowledge_graph.py src/entity_mapping/models/__init__.py
git commit -m "feat: add KnowledgeGraph model with export methods

- Create KnowledgeGraph and GraphMetadata models
- Implement to_json() for JSON export
- Implement to_summary() for natural language summaries

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## Task 5: Stage 1 - Entity Extraction Prompt

**Goal:** Design prompt for entity extraction with coreference resolution

**Files:**
- Create: `src/entity_mapping/prompts/entity_extraction.py`
- Modify: `src/entity_mapping/prompts/__init__.py`

### Step 1: Implement entity extraction prompts

File: `src/entity_mapping/prompts/entity_extraction.py`

```python
"""Prompts for entity extraction stage."""

SYSTEM_PROMPT = """You are an expert at identifying and extracting named entities from text.

Your task is to:
1. Extract ALL entities mentioned in the text
2. Resolve coreferences (pronouns, abbreviations, aliases to canonical forms)
3. Classify each entity's type accurately
4. Track all mentions of each entity

Rules:
- Use canonical forms (full names, not abbreviations)
  Example: "TechCorp" not "TC", "Sarah Johnson" not "Sarah"
- Classify entity types accurately using these categories:
  PERSON, ORGANIZATION, LOCATION, PRODUCT, EVENT, CONCEPT, DATE, OTHER
- Track all textual mentions of each entity
  Example: "Sarah Johnson" → mentions: ["Sarah", "she", "the founder", "Sarah Johnson"]
- Be conservative - only extract clearly identifiable entities
- Deduplicate: "TechCorp" and "TechCorp GmbH" should be one entity
- For ambiguous cases, use context to disambiguate

Output Format:
Return a JSON array of entities, each with:
- text: canonical name
- type: entity category
- mentions: list of all text spans referring to this entity
"""

USER_PROMPT_TEMPLATE = """Extract all entities from the following text.

Text:
{text}

{context_section}

Return JSON array of entities:
[
  {{
    "text": "canonical entity name",
    "type": "PERSON|ORGANIZATION|LOCATION|PRODUCT|EVENT|CONCEPT|DATE|OTHER",
    "mentions": ["mention1", "mention2", ...]
  }}
]
"""

CONTEXT_SECTION_TEMPLATE = """
Additional Context:
{context}
"""


def build_entity_extraction_prompt(text: str, context: str = None) -> dict:
    """Build entity extraction prompt.

    Args:
        text: The text to extract entities from
        context: Optional additional context

    Returns:
        Dictionary with 'system' and 'user' prompts
    """
    context_section = ""
    if context:
        context_section = CONTEXT_SECTION_TEMPLATE.format(context=context)

    user_prompt = USER_PROMPT_TEMPLATE.format(
        text=text,
        context_section=context_section
    )

    return {
        "system": SYSTEM_PROMPT,
        "user": user_prompt
    }
```

### Step 2: Update __init__.py

File: `src/entity_mapping/prompts/__init__.py`

```python
"""Prompts for entity relationship mapping stages."""

from src.entity_mapping.prompts.entity_extraction import (
    SYSTEM_PROMPT as ENTITY_EXTRACTION_SYSTEM_PROMPT,
    USER_PROMPT_TEMPLATE as ENTITY_EXTRACTION_USER_TEMPLATE,
    build_entity_extraction_prompt
)

__all__ = [
    "ENTITY_EXTRACTION_SYSTEM_PROMPT",
    "ENTITY_EXTRACTION_USER_TEMPLATE",
    "build_entity_extraction_prompt"
]
```

### Step 3: Commit entity extraction prompts

```bash
git add src/entity_mapping/prompts/entity_extraction.py src/entity_mapping/prompts/__init__.py
git commit -m "feat: add entity extraction prompts

- Create system prompt for entity extraction with coreference resolution
- Create user prompt template with optional context
- Build helper function for prompt construction
- Focus on canonical forms and deduplication

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## Task 6: Stage 1 - Entity Extraction Agent

**Goal:** Implement LangChain agent for entity extraction

**Files:**
- Create: `src/entity_mapping/stages/entity_extraction.py`
- Modify: `src/entity_mapping/stages/__init__.py`

### Step 1: Implement entity extraction agent

File: `src/entity_mapping/stages/entity_extraction.py`

```python
"""Entity extraction stage using LangChain."""

import os
from typing import List, Optional
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.prompts import ChatPromptTemplate

from src.entity_mapping.models.entity import Entity, EntityType
from src.entity_mapping.prompts.entity_extraction import build_entity_extraction_prompt


class EntityExtractionOutput(BaseModel):
    """Structured output from entity extraction."""
    entities: List[dict]


class EntityExtractionStage:
    """Stage 1: Extract entities from text with coreference resolution."""

    def __init__(
        self,
        model: str = "gpt-5-nano-2025-08-07",
        temperature: float = 0.0
    ):
        """Initialize entity extraction stage.

        Args:
            model: LLM model to use
            temperature: Sampling temperature (0.0 for deterministic)
        """
        self.model_name = model
        self.temperature = temperature
        self.llm = self._initialize_llm()

    def _initialize_llm(self):
        """Initialize LangChain LLM client."""
        if "gpt" in self.model_name or "o1" in self.model_name:
            return ChatOpenAI(
                model=self.model_name,
                temperature=self.temperature,
                api_key=os.getenv("OPENAI_API_KEY")
            )
        elif "claude" in self.model_name:
            return ChatAnthropic(
                model=self.model_name,
                temperature=self.temperature,
                api_key=os.getenv("ANTHROPIC_API_KEY")
            )
        else:
            raise ValueError(f"Unsupported model: {self.model_name}")

    def extract_entities(
        self,
        text: str,
        context: Optional[str] = None
    ) -> List[Entity]:
        """Extract entities from text.

        Args:
            text: The text to extract entities from
            context: Optional contextual information

        Returns:
            List of extracted Entity objects
        """
        # Build prompt
        prompts = build_entity_extraction_prompt(text, context)

        # Create LangChain prompt template
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", prompts["system"]),
            ("user", prompts["user"])
        ])

        # Create structured output chain
        structured_llm = self.llm.with_structured_output(EntityExtractionOutput)
        chain = prompt_template | structured_llm

        # Invoke chain
        result = chain.invoke({})

        # Convert to Entity objects with IDs
        entities = []
        for i, entity_dict in enumerate(result.entities, start=1):
            entity = Entity(
                id=f"e{i}",
                text=entity_dict["text"],
                type=EntityType(entity_dict["type"]),
                mentions=entity_dict.get("mentions", [entity_dict["text"]]),
                context=context
            )
            entities.append(entity)

        return entities
```

### Step 2: Update __init__.py

File: `src/entity_mapping/stages/__init__.py`

```python
"""Pipeline stages for entity relationship mapping."""

from src.entity_mapping.stages.entity_extraction import EntityExtractionStage

__all__ = ["EntityExtractionStage"]
```

### Step 3: Commit entity extraction stage

```bash
git add src/entity_mapping/stages/entity_extraction.py src/entity_mapping/stages/__init__.py
git commit -m "feat: implement entity extraction stage

- Create EntityExtractionStage with LangChain integration
- Support OpenAI and Anthropic models
- Use structured output for reliable entity extraction
- Assign unique IDs to entities (e1, e2, ...)
- Handle coreference resolution via LLM

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## Task 7: Stage 2 - Relationship Extraction Prompt

**Goal:** Design prompt for extracting explicit relationships only

**Files:**
- Create: `src/entity_mapping/prompts/relationship_extraction.py`
- Modify: `src/entity_mapping/prompts/__init__.py`

### Step 1: Implement relationship extraction prompts

File: `src/entity_mapping/prompts/relationship_extraction.py`

```python
"""Prompts for explicit relationship extraction stage."""

SYSTEM_PROMPT = """You are an expert at extracting relationships that are EXPLICITLY stated in text.

Your task is to:
1. Identify relationships between entities that are directly mentioned in the text
2. Extract the relationship type and supporting evidence
3. Do NOT infer or guess relationships - only extract what is explicitly stated

Rules:
- Every relationship must have direct textual evidence
- Use clear relationship types (founded, works_at, located_in, part_of, etc.)
- Provide the exact text span that states the relationship
- If a relationship is ambiguous or implicit, SKIP it (Stage 3 handles inference)
- Only extract relationships between entities that were identified in Stage 1

Output Format:
Return a JSON array of relationships, each with:
- source_entity_id: ID of source entity
- target_entity_id: ID of target entity
- relationship_type: type of relationship
- evidence: exact text supporting the relationship
"""

USER_PROMPT_TEMPLATE = """Extract all EXPLICIT relationships from the text.

Text:
{text}

Entities:
{entities_list}

Return JSON array of relationships:
[
  {{
    "source_entity_id": "e1",
    "target_entity_id": "e2",
    "relationship_type": "founded|works_at|located_in|etc",
    "evidence": "exact text span from source"
  }}
]

Remember: ONLY extract relationships that are explicitly stated. Do not infer.
"""


def build_relationship_extraction_prompt(text: str, entities: list) -> dict:
    """Build relationship extraction prompt.

    Args:
        text: The original text
        entities: List of Entity objects from Stage 1

    Returns:
        Dictionary with 'system' and 'user' prompts
    """
    # Format entities for prompt
    entities_list = "\n".join([
        f"- {e.id}: {e.text} ({e.type})"
        for e in entities
    ])

    user_prompt = USER_PROMPT_TEMPLATE.format(
        text=text,
        entities_list=entities_list
    )

    return {
        "system": SYSTEM_PROMPT,
        "user": user_prompt
    }
```

### Step 2: Update __init__.py

File: `src/entity_mapping/prompts/__init__.py`

```python
"""Prompts for entity relationship mapping stages."""

from src.entity_mapping.prompts.entity_extraction import (
    SYSTEM_PROMPT as ENTITY_EXTRACTION_SYSTEM_PROMPT,
    USER_PROMPT_TEMPLATE as ENTITY_EXTRACTION_USER_TEMPLATE,
    build_entity_extraction_prompt
)
from src.entity_mapping.prompts.relationship_extraction import (
    SYSTEM_PROMPT as RELATIONSHIP_EXTRACTION_SYSTEM_PROMPT,
    USER_PROMPT_TEMPLATE as RELATIONSHIP_EXTRACTION_USER_TEMPLATE,
    build_relationship_extraction_prompt
)

__all__ = [
    "ENTITY_EXTRACTION_SYSTEM_PROMPT",
    "ENTITY_EXTRACTION_USER_TEMPLATE",
    "build_entity_extraction_prompt",
    "RELATIONSHIP_EXTRACTION_SYSTEM_PROMPT",
    "RELATIONSHIP_EXTRACTION_USER_TEMPLATE",
    "build_relationship_extraction_prompt"
]
```

### Step 3: Commit relationship extraction prompts

```bash
git add src/entity_mapping/prompts/relationship_extraction.py src/entity_mapping/prompts/__init__.py
git commit -m "feat: add relationship extraction prompts

- Create system prompt emphasizing EXPLICIT relationships only
- Create user prompt template with entity list
- Build helper function for prompt construction
- Clear guidance to avoid inference (handled in Stage 3)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## Task 8: Stage 2 - Relationship Extraction Agent

**Goal:** Implement LangChain agent for explicit relationship extraction

**Files:**
- Create: `src/entity_mapping/stages/relationship_extraction.py`
- Modify: `src/entity_mapping/stages/__init__.py`

### Step 1: Implement relationship extraction agent

File: `src/entity_mapping/stages/relationship_extraction.py`

```python
"""Explicit relationship extraction stage using LangChain."""

import os
from typing import List
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.prompts import ChatPromptTemplate

from src.entity_mapping.models.entity import Entity
from src.entity_mapping.models.relationship import Relationship
from src.entity_mapping.prompts.relationship_extraction import (
    build_relationship_extraction_prompt
)


class RelationshipExtractionOutput(BaseModel):
    """Structured output from relationship extraction."""
    relationships: List[dict]


class RelationshipExtractionStage:
    """Stage 2: Extract explicit relationships from text."""

    def __init__(
        self,
        model: str = "gpt-5-nano-2025-08-07",
        temperature: float = 0.0
    ):
        """Initialize relationship extraction stage.

        Args:
            model: LLM model to use
            temperature: Sampling temperature (0.0 for deterministic)
        """
        self.model_name = model
        self.temperature = temperature
        self.llm = self._initialize_llm()

    def _initialize_llm(self):
        """Initialize LangChain LLM client."""
        if "gpt" in self.model_name or "o1" in self.model_name:
            return ChatOpenAI(
                model=self.model_name,
                temperature=self.temperature,
                api_key=os.getenv("OPENAI_API_KEY")
            )
        elif "claude" in self.model_name:
            return ChatAnthropic(
                model=self.model_name,
                temperature=self.temperature,
                api_key=os.getenv("ANTHROPIC_API_KEY")
            )
        else:
            raise ValueError(f"Unsupported model: {self.model_name}")

    def extract_relationships(
        self,
        text: str,
        entities: List[Entity]
    ) -> List[Relationship]:
        """Extract explicit relationships from text.

        Args:
            text: The original text
            entities: List of entities from Stage 1

        Returns:
            List of explicit Relationship objects
        """
        if not entities:
            return []

        # Build prompt
        prompts = build_relationship_extraction_prompt(text, entities)

        # Create LangChain prompt template
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", prompts["system"]),
            ("user", prompts["user"])
        ])

        # Create structured output chain
        structured_llm = self.llm.with_structured_output(RelationshipExtractionOutput)
        chain = prompt_template | structured_llm

        # Invoke chain
        result = chain.invoke({})

        # Convert to Relationship objects (all explicit)
        relationships = []
        for rel_dict in result.relationships:
            relationship = Relationship(
                source_entity_id=rel_dict["source_entity_id"],
                target_entity_id=rel_dict["target_entity_id"],
                relationship_type=rel_dict["relationship_type"],
                evidence=rel_dict["evidence"],
                is_inferred=False,  # Stage 2 only extracts explicit
                confidence=1.0      # Explicit relationships always 1.0
            )
            relationships.append(relationship)

        return relationships
```

### Step 2: Update __init__.py

File: `src/entity_mapping/stages/__init__.py`

```python
"""Pipeline stages for entity relationship mapping."""

from src.entity_mapping.stages.entity_extraction import EntityExtractionStage
from src.entity_mapping.stages.relationship_extraction import RelationshipExtractionStage

__all__ = [
    "EntityExtractionStage",
    "RelationshipExtractionStage"
]
```

### Step 3: Commit relationship extraction stage

```bash
git add src/entity_mapping/stages/relationship_extraction.py src/entity_mapping/stages/__init__.py
git commit -m "feat: implement relationship extraction stage

- Create RelationshipExtractionStage with LangChain integration
- Extract only explicit relationships (is_inferred=False)
- All explicit relationships have confidence=1.0
- Handle empty entity lists gracefully

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## Task 9: Stage 3 - Relationship Inference Prompt

**Goal:** Design prompt for inferring implicit relationships

**Files:**
- Create: `src/entity_mapping/prompts/relationship_inference.py`
- Modify: `src/entity_mapping/prompts/__init__.py`

### Step 1: Implement relationship inference prompts

File: `src/entity_mapping/prompts/relationship_inference.py`

```python
"""Prompts for relationship inference stage."""

SYSTEM_PROMPT = """You are an expert at inferring implicit relationships using logical reasoning.

Your task is to:
1. Identify entity pairs that co-occur but lack explicit relationships
2. Infer logical relationships based on context and common sense
3. Provide confidence scores and reasoning for each inference

Rules:
- Only infer relationships with high confidence (>0.7)
- Always provide clear reasoning/justification
- Conservative approach: when uncertain, don't infer
- Consider context and common-sense knowledge
- Examples of valid inferences:
  * "hired as CTO" → infers "works_at" (confidence: 0.95)
  * "CEO of X" + "X based in Berlin" → infers "located_in" (confidence: 0.90)

Output Format:
Return a JSON array of inferred relationships, each with:
- source_entity_id: ID of source entity
- target_entity_id: ID of target entity
- relationship_type: inferred relationship type
- evidence: text that supports the inference
- confidence: score between 0.7 and 1.0
- reasoning: explanation of why this relationship was inferred
"""

USER_PROMPT_TEMPLATE = """Infer implicit relationships from the text.

Text:
{text}

Entities:
{entities_list}

Existing Explicit Relationships:
{existing_relationships}

Identify entity pairs that co-occur but have no explicit relationship, and infer logical connections.

Return JSON array of inferred relationships:
[
  {{
    "source_entity_id": "e1",
    "target_entity_id": "e2",
    "relationship_type": "inferred_type",
    "evidence": "text supporting inference",
    "confidence": 0.85,
    "reasoning": "explanation of inference"
  }}
]

Only include inferences with confidence > 0.7. Be conservative.
"""


def build_relationship_inference_prompt(
    text: str,
    entities: list,
    existing_relationships: list
) -> dict:
    """Build relationship inference prompt.

    Args:
        text: The original text
        entities: List of Entity objects
        existing_relationships: List of Relationship objects from Stage 2

    Returns:
        Dictionary with 'system' and 'user' prompts
    """
    # Format entities for prompt
    entities_list = "\n".join([
        f"- {e.id}: {e.text} ({e.type})"
        for e in entities
    ])

    # Format existing relationships
    if existing_relationships:
        rel_lines = [
            f"- {r.source_entity_id} → {r.target_entity_id}: {r.relationship_type}"
            for r in existing_relationships
        ]
        existing_rels_str = "\n".join(rel_lines)
    else:
        existing_rels_str = "(none)"

    user_prompt = USER_PROMPT_TEMPLATE.format(
        text=text,
        entities_list=entities_list,
        existing_relationships=existing_rels_str
    )

    return {
        "system": SYSTEM_PROMPT,
        "user": user_prompt
    }
```

### Step 2: Update __init__.py

File: `src/entity_mapping/prompts/__init__.py`

```python
"""Prompts for entity relationship mapping stages."""

from src.entity_mapping.prompts.entity_extraction import (
    SYSTEM_PROMPT as ENTITY_EXTRACTION_SYSTEM_PROMPT,
    USER_PROMPT_TEMPLATE as ENTITY_EXTRACTION_USER_TEMPLATE,
    build_entity_extraction_prompt
)
from src.entity_mapping.prompts.relationship_extraction import (
    SYSTEM_PROMPT as RELATIONSHIP_EXTRACTION_SYSTEM_PROMPT,
    USER_PROMPT_TEMPLATE as RELATIONSHIP_EXTRACTION_USER_TEMPLATE,
    build_relationship_extraction_prompt
)
from src.entity_mapping.prompts.relationship_inference import (
    SYSTEM_PROMPT as RELATIONSHIP_INFERENCE_SYSTEM_PROMPT,
    USER_PROMPT_TEMPLATE as RELATIONSHIP_INFERENCE_USER_TEMPLATE,
    build_relationship_inference_prompt
)

__all__ = [
    "ENTITY_EXTRACTION_SYSTEM_PROMPT",
    "ENTITY_EXTRACTION_USER_TEMPLATE",
    "build_entity_extraction_prompt",
    "RELATIONSHIP_EXTRACTION_SYSTEM_PROMPT",
    "RELATIONSHIP_EXTRACTION_USER_TEMPLATE",
    "build_relationship_extraction_prompt",
    "RELATIONSHIP_INFERENCE_SYSTEM_PROMPT",
    "RELATIONSHIP_INFERENCE_USER_TEMPLATE",
    "build_relationship_inference_prompt"
]
```

### Step 3: Commit relationship inference prompts

```bash
git add src/entity_mapping/prompts/relationship_inference.py src/entity_mapping/prompts/__init__.py
git commit -m "feat: add relationship inference prompts

- Create system prompt for conservative LLM-based inference
- Require confidence > 0.7 and reasoning for all inferences
- Include existing relationships to avoid duplication
- Provide examples of valid inferences

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## Task 10: Stage 3 - Relationship Inference Agent

**Goal:** Implement LangChain agent for relationship inference

**Files:**
- Create: `src/entity_mapping/stages/relationship_inference.py`
- Modify: `src/entity_mapping/stages/__init__.py`

### Step 1: Implement relationship inference agent

File: `src/entity_mapping/stages/relationship_inference.py`

```python
"""Relationship inference stage using LangChain."""

import os
from typing import List
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.prompts import ChatPromptTemplate

from src.entity_mapping.models.entity import Entity
from src.entity_mapping.models.relationship import Relationship
from src.entity_mapping.prompts.relationship_inference import (
    build_relationship_inference_prompt
)


class RelationshipInferenceOutput(BaseModel):
    """Structured output from relationship inference."""
    relationships: List[dict]


class RelationshipInferenceStage:
    """Stage 3: Infer implicit relationships using LLM reasoning."""

    def __init__(
        self,
        model: str = "gpt-5-nano-2025-08-07",
        temperature: float = 0.0,
        confidence_threshold: float = 0.7
    ):
        """Initialize relationship inference stage.

        Args:
            model: LLM model to use
            temperature: Sampling temperature (0.0 for deterministic)
            confidence_threshold: Minimum confidence for inferred relationships
        """
        self.model_name = model
        self.temperature = temperature
        self.confidence_threshold = confidence_threshold
        self.llm = self._initialize_llm()

    def _initialize_llm(self):
        """Initialize LangChain LLM client."""
        if "gpt" in self.model_name or "o1" in self.model_name:
            return ChatOpenAI(
                model=self.model_name,
                temperature=self.temperature,
                api_key=os.getenv("OPENAI_API_KEY")
            )
        elif "claude" in self.model_name:
            return ChatAnthropic(
                model=self.model_name,
                temperature=self.temperature,
                api_key=os.getenv("ANTHROPIC_API_KEY")
            )
        else:
            raise ValueError(f"Unsupported model: {self.model_name}")

    def infer_relationships(
        self,
        text: str,
        entities: List[Entity],
        existing_relationships: List[Relationship]
    ) -> List[Relationship]:
        """Infer implicit relationships from text.

        Args:
            text: The original text
            entities: List of entities from Stage 1
            existing_relationships: Explicit relationships from Stage 2

        Returns:
            List of inferred Relationship objects
        """
        if not entities:
            return []

        # Build prompt
        prompts = build_relationship_inference_prompt(
            text,
            entities,
            existing_relationships
        )

        # Create LangChain prompt template
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", prompts["system"]),
            ("user", prompts["user"])
        ])

        # Create structured output chain
        structured_llm = self.llm.with_structured_output(RelationshipInferenceOutput)
        chain = prompt_template | structured_llm

        # Invoke chain
        result = chain.invoke({})

        # Convert to Relationship objects (all inferred)
        relationships = []
        for rel_dict in result.relationships:
            confidence = rel_dict.get("confidence", 0.0)

            # Filter by confidence threshold
            if confidence < self.confidence_threshold:
                continue

            relationship = Relationship(
                source_entity_id=rel_dict["source_entity_id"],
                target_entity_id=rel_dict["target_entity_id"],
                relationship_type=rel_dict["relationship_type"],
                evidence=rel_dict["evidence"],
                is_inferred=True,  # Stage 3 only produces inferred
                confidence=confidence,
                reasoning=rel_dict["reasoning"]
            )
            relationships.append(relationship)

        return relationships
```

### Step 2: Update __init__.py

File: `src/entity_mapping/stages/__init__.py`

```python
"""Pipeline stages for entity relationship mapping."""

from src.entity_mapping.stages.entity_extraction import EntityExtractionStage
from src.entity_mapping.stages.relationship_extraction import RelationshipExtractionStage
from src.entity_mapping.stages.relationship_inference import RelationshipInferenceStage

__all__ = [
    "EntityExtractionStage",
    "RelationshipExtractionStage",
    "RelationshipInferenceStage"
]
```

### Step 3: Commit relationship inference stage

```bash
git add src/entity_mapping/stages/relationship_inference.py src/entity_mapping/stages/__init__.py
git commit -m "feat: implement relationship inference stage

- Create RelationshipInferenceStage with LLM reasoning
- Infer implicit relationships (is_inferred=True)
- Filter by configurable confidence threshold (default 0.7)
- All inferred relationships include reasoning

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## Task 11: Pipeline Integration

**Goal:** Create EntityMappingPipeline orchestrating all 3 stages

**Files:**
- Create: `src/entity_mapping/pipeline.py`
- Modify: `src/entity_mapping/__init__.py`

### Step 1: Implement pipeline

File: `src/entity_mapping/pipeline.py`

```python
"""Entity Relationship Mapping Pipeline - orchestrates all stages."""

from typing import Optional
from src.entity_mapping.models import KnowledgeGraph, GraphMetadata
from src.entity_mapping.stages import (
    EntityExtractionStage,
    RelationshipExtractionStage,
    RelationshipInferenceStage
)


class EntityMappingPipeline:
    """Complete 3-stage pipeline for entity relationship mapping.

    Stages:
    1. Entity Extraction - identify and normalize entities
    2. Relationship Extraction - extract explicit relationships
    3. Relationship Inference - infer implicit relationships
    """

    def __init__(
        self,
        model: str = "gpt-5-nano-2025-08-07",
        temperature: float = 0.0,
        confidence_threshold: float = 0.7,
        include_inferred: bool = True
    ):
        """Initialize the entity mapping pipeline.

        Args:
            model: LLM model to use for all stages
            temperature: Sampling temperature (0.0 for deterministic)
            confidence_threshold: Minimum confidence for inferred relationships
            include_inferred: Whether to run Stage 3 (inference)
        """
        self.model = model
        self.temperature = temperature
        self.confidence_threshold = confidence_threshold
        self.include_inferred = include_inferred

        # Initialize stages
        self.stage1 = EntityExtractionStage(model, temperature)
        self.stage2 = RelationshipExtractionStage(model, temperature)
        self.stage3 = RelationshipInferenceStage(
            model,
            temperature,
            confidence_threshold
        )

    def extract_knowledge_graph(
        self,
        text: str,
        context: Optional[str] = None
    ) -> KnowledgeGraph:
        """Extract complete knowledge graph from text.

        Args:
            text: The text to analyze
            context: Optional contextual information

        Returns:
            KnowledgeGraph with entities and relationships
        """
        # Stage 1: Extract entities
        entities = self.stage1.extract_entities(text, context)

        # Stage 2: Extract explicit relationships
        explicit_relationships = self.stage2.extract_relationships(text, entities)

        # Stage 3: Infer implicit relationships (if enabled)
        inferred_relationships = []
        if self.include_inferred:
            inferred_relationships = self.stage3.infer_relationships(
                text,
                entities,
                explicit_relationships
            )

        # Combine all relationships
        all_relationships = explicit_relationships + inferred_relationships

        # Create metadata
        metadata = GraphMetadata(
            model_used=self.model,
            total_entities=len(entities),
            total_relationships=len(all_relationships),
            explicit_relationships=len(explicit_relationships),
            inferred_relationships=len(inferred_relationships)
        )

        # Build knowledge graph
        knowledge_graph = KnowledgeGraph(
            entities=entities,
            relationships=all_relationships,
            metadata=metadata
        )

        return knowledge_graph
```

### Step 2: Update __init__.py

File: `src/entity_mapping/__init__.py`

```python
"""Entity Relationship Mapping - extract knowledge graphs from text."""

from src.entity_mapping.pipeline import EntityMappingPipeline
from src.entity_mapping.models import (
    Entity,
    EntityType,
    Relationship,
    KnowledgeGraph,
    GraphMetadata
)

__all__ = [
    "EntityMappingPipeline",
    "Entity",
    "EntityType",
    "Relationship",
    "KnowledgeGraph",
    "GraphMetadata"
]
```

### Step 3: Commit pipeline

```bash
git add src/entity_mapping/pipeline.py src/entity_mapping/__init__.py
git commit -m "feat: implement EntityMappingPipeline

- Orchestrate all 3 stages (entity extraction, explicit rels, inferred rels)
- Support optional inference (include_inferred parameter)
- Generate complete KnowledgeGraph with metadata
- Main entry point for entity mapping feature

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## Task 12: MCP Server Implementation

**Goal:** Create MCP server exposing entity mapping tools

**Files:**
- Create: `mcp_servers/entity_mapping_server.py`

### Step 1: Implement MCP server

File: `mcp_servers/entity_mapping_server.py`

```python
#!/usr/bin/env python3
"""Entity Mapping MCP Server - STDIO-based integration for Claude Code."""

import os
import sys
import json
import asyncio
from typing import Any

# MCP SDK imports
from mcp.server import Server
from mcp.types import Tool, TextContent

# Entity mapping imports
from src.entity_mapping import EntityMappingPipeline, KnowledgeGraph


# Initialize server
server = Server("entity-mapping")


def validate_input(text: str) -> None:
    """Validate input text.

    Args:
        text: Input text to validate

    Raises:
        ValueError: If validation fails
    """
    if not text or len(text.strip()) == 0:
        raise ValueError("Text cannot be empty")
    if len(text) > 50000:  # ~50KB limit
        raise ValueError("Text too long (max 50,000 characters)")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="extract_entities_and_relationships",
            description=(
                "Extract entities and relationships from unstructured text using a 3-stage pipeline. "
                "Stage 1: Entity extraction with coreference resolution. "
                "Stage 2: Explicit relationship extraction. "
                "Stage 3: Implicit relationship inference using LLM reasoning. "
                "Returns a knowledge graph with both JSON and natural language summary."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to analyze (max 50,000 characters)"
                    },
                    "context": {
                        "type": "string",
                        "description": "Optional contextual information (e.g., original question)"
                    },
                    "model": {
                        "type": "string",
                        "description": "Optional LLM model to use (default: gpt-5-nano-2025-08-07)",
                        "default": "gpt-5-nano-2025-08-07"
                    },
                    "include_inferred": {
                        "type": "boolean",
                        "description": "Whether to include inferred relationships (default: true)",
                        "default": True
                    },
                    "confidence_threshold": {
                        "type": "number",
                        "description": "Minimum confidence for inferred relationships (default: 0.7)",
                        "default": 0.7,
                        "minimum": 0.0,
                        "maximum": 1.0
                    }
                },
                "required": ["text"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Handle tool calls.

    Args:
        name: Tool name
        arguments: Tool arguments

    Returns:
        List of TextContent responses
    """
    if name != "extract_entities_and_relationships":
        raise ValueError(f"Unknown tool: {name}")

    try:
        # Extract arguments
        text = arguments.get("text", "")
        context = arguments.get("context")
        model = arguments.get("model", os.getenv("ENTITY_MAPPING_MODEL", "gpt-5-nano-2025-08-07"))
        include_inferred = arguments.get("include_inferred", True)
        confidence_threshold = arguments.get("confidence_threshold", 0.7)

        # Validate input
        validate_input(text)

        # Initialize pipeline
        pipeline = EntityMappingPipeline(
            model=model,
            temperature=0.0,
            confidence_threshold=confidence_threshold,
            include_inferred=include_inferred
        )

        # Extract knowledge graph
        knowledge_graph: KnowledgeGraph = pipeline.extract_knowledge_graph(
            text=text,
            context=context
        )

        # Format output as markdown with both summary and JSON
        output_lines = ["# Entity Relationship Mapping Results\n"]

        # Natural language summary
        output_lines.append("## Summary\n")
        output_lines.append(knowledge_graph.to_summary())
        output_lines.append("\n")

        # Metadata
        output_lines.append("## Metadata\n")
        output_lines.append(f"- **Model used:** {knowledge_graph.metadata.model_used}")
        output_lines.append(f"- **Total entities:** {knowledge_graph.metadata.total_entities}")
        output_lines.append(f"- **Total relationships:** {knowledge_graph.metadata.total_relationships}")
        output_lines.append(f"- **Explicit relationships:** {knowledge_graph.metadata.explicit_relationships}")
        output_lines.append(f"- **Inferred relationships:** {knowledge_graph.metadata.inferred_relationships}")
        output_lines.append(f"- **Created at:** {knowledge_graph.metadata.created_at}")
        output_lines.append("\n")

        # JSON export
        output_lines.append("## JSON Export\n")
        output_lines.append("```json")
        output_lines.append(json.dumps(knowledge_graph.to_json(), indent=2))
        output_lines.append("```\n")

        formatted_output = "\n".join(output_lines)

        return [
            TextContent(
                type="text",
                text=formatted_output
            )
        ]

    except Exception as e:
        # Return error as formatted text
        error_output = f"""# Entity Mapping Error

**Error:** {str(e)}

**Suggestions:**
- Check that your API key (OPENAI_API_KEY or ANTHROPIC_API_KEY) is set
- Ensure the input text is not empty and under 50,000 characters
- Verify your API key has sufficient credits
- Try a different model if the current one is unavailable

**Need help?** Check the documentation at https://github.com/mhornd/claimification
"""
        return [
            TextContent(
                type="text",
                text=error_output
            )
        ]


async def main():
    """Main entry point for the MCP server."""
    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
```

### Step 2: Make server executable

```bash
chmod +x mcp_servers/entity_mapping_server.py
```

### Step 3: Commit MCP server

```bash
git add mcp_servers/entity_mapping_server.py
git commit -m "feat: implement entity mapping MCP server

- Create extract_entities_and_relationships tool
- Output both natural language summary and JSON
- Support configurable model, confidence threshold, and inference toggle
- Follow same error handling pattern as claim extraction server

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## Task 13: Update Main README

**Goal:** Update README to document both features

**Files:**
- Modify: `README.md`

### Step 1: Update README

File: `README.md`

Update the title and description (lines 1-9):

```markdown
# Claimification

> **Extract verifiable factual claims and map entity relationships from text using multi-stage AI pipelines**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/LangChain-Enabled-green.svg)](https://langchain.com/)

Claimification is a Claude Code plugin providing two powerful text analysis features:
1. **Claim Extraction** - Extract verifiable factual claims using a 4-stage pipeline
2. **Entity Relationship Mapping** - Extract entities and relationships to build knowledge graphs
```

Add after line 20 (after existing "Why Claimification?" section):

```markdown
## Features

### 1. Claim Extraction

Extract verifiable factual claims from LLM outputs using a sophisticated 4-stage pipeline based on research from Microsoft Research.

✅ **Extracting verifiable facts** from complex LLM outputs
✅ **Filtering out opinions** and non-verifiable content
✅ **Resolving ambiguities** using contextual information
✅ **Creating standalone claims** that preserve critical context
✅ **Flagging unresolvable ambiguities** instead of guessing

### 2. Entity Relationship Mapping

Transform unstructured text into queryable knowledge graphs by extracting entities and their relationships.

📊 **Structure Chaos** - Convert LLM outputs into queryable knowledge structures
🔗 **Discover Connections** - Find both explicit and implicit relationships
🎯 **Multiple Formats** - Export as JSON or natural language summaries
🤖 **LLM-Powered Inference** - Infer implicit relationships with confidence scores

## Dual MCP Servers

Claimification exposes both features through separate MCP servers:
- **claim-extraction** - Extract verifiable claims
- **entity-mapping** - Map entity relationships

Both can be used independently or together for comprehensive text analysis.
```

Update "Using as a Claude Code Plugin" section (around line 47):

```markdown
### Using as a Claude Code Plugin

```bash
# Install the plugin in Claude Code
/plugin install claimification

# Use claim extraction
/extract-claims

# Use entity mapping
# (Available through MCP tool: extract_entities_and_relationships)
```
```

### Step 2: Commit README update

```bash
git add README.md
git commit -m "docs: update README for dual-feature plugin

- Document both claim extraction and entity mapping features
- Explain dual MCP server architecture
- Update feature descriptions and benefits
- Clarify independent usage of both features

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## Task 14: Create Entity Mapping Documentation

**Goal:** Write comprehensive documentation for entity mapping feature

**Files:**
- Create: `docs/entity_mapping/USAGE.md`
- Create: `docs/entity_mapping/API.md`

### Step 1: Create usage guide

File: `docs/entity_mapping/USAGE.md`

```markdown
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
```

### Step 2: Create API reference

File: `docs/entity_mapping/API.md`

```markdown
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
```

### Step 3: Commit documentation

```bash
git add docs/entity_mapping/
git commit -m "docs: add entity mapping usage guide and API reference

- Create comprehensive usage guide with examples
- Document all 3 pipeline stages
- Explain configuration options and output formats
- Provide API reference for all classes and methods

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## Completion

All tasks complete! The Entity Relationship Mapper is now fully implemented with:

✅ Repository restructured for dual MCP servers
✅ Complete data models (Entity, Relationship, KnowledgeGraph)
✅ All 3 pipeline stages implemented
✅ MCP server exposing entity mapping tools
✅ Comprehensive documentation

**Next Steps:**
1. Test the implementation with real examples
2. Verify MCP server integration with Claude Code
3. Iterate on prompts based on real-world performance
4. Consider adding visualization utilities (future enhancement)
