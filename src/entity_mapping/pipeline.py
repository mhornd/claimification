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
