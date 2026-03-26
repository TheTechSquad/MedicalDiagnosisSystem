from typing import Dict, List, Set

from medical_expert.models import DiagnosisResult, DiseaseRule


class ForwardChainingEngine:
    """Simple forward chaining engine for medical diagnosis rules."""

    def __init__(self, rules: List[DiseaseRule]) -> None:
        self.rules = rules

    def diagnose(self, symptom_facts: Dict[str, bool]) -> List[DiagnosisResult]:
        true_symptoms = self._extract_true_symptoms(symptom_facts)

        inferred_diagnoses: List[DiagnosisResult] = []
        inferred_names: Set[str] = set()

        # Continue firing rules until no new diagnosis can be inferred.
        changed = True
        while changed:
            changed = False
            for rule in self.rules:
                if rule.disease in inferred_names:
                    continue

                if rule.required_symptoms.issubset(true_symptoms):
                    result = self._build_result(rule, true_symptoms)
                    inferred_diagnoses.append(result)
                    inferred_names.add(rule.disease)
                    changed = True

        return sorted(inferred_diagnoses, key=lambda item: item.confidence, reverse=True)

    @staticmethod
    def _extract_true_symptoms(symptom_facts: Dict[str, bool]) -> Set[str]:
        return {name for name, value in symptom_facts.items() if value}

    @staticmethod
    def _build_result(rule: DiseaseRule, true_symptoms: Set[str]) -> DiagnosisResult:
        matched_required = sorted(rule.required_symptoms.intersection(true_symptoms))
        matched_optional = sorted(rule.optional_symptoms.intersection(true_symptoms))

        # Required symptoms have full weight; optional ones contribute partial support.
        required_score = len(matched_required)
        optional_score = 0.5 * len(matched_optional)
        max_score = len(rule.required_symptoms) + (0.5 * len(rule.optional_symptoms))
        confidence = (required_score + optional_score) / max_score if max_score else 0.0

        return DiagnosisResult(
            disease=rule.disease,
            confidence=round(confidence * 100, 1),
            matched_required=matched_required,
            matched_optional=matched_optional,
            explanation=rule.explanation,
        )
