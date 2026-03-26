from dataclasses import dataclass
from typing import List, Set


@dataclass(frozen=True)
class DiseaseRule:
    """Represents one diagnosis rule in the knowledge base."""

    disease: str
    required_symptoms: Set[str]
    optional_symptoms: Set[str]
    explanation: str


@dataclass
class DiagnosisResult:
    """Stores one inferred diagnosis and supporting details."""

    disease: str
    confidence: float
    matched_required: List[str]
    matched_optional: List[str]
    explanation: str
