# System Report

## 1. Project Overview
A rule-based medical diagnosis expert system was developed in Python to demonstrate knowledge representation, inference, and user interaction in AI expert systems.

## 2. Design Decisions
- Chosen language: Python for readability and rapid development.
- Architecture:
  - Knowledge base module (`knowledge_base.py`)
  - Inference engine module (`inference_engine.py`)
  - User interface module (`gui.py`)
- Rule design: each disease has required and optional symptoms.

## 3. Inference Mechanism
- Forward chaining starts from user-provided symptom facts.
- Rules are checked iteratively.
- If all required symptoms of a rule are present, diagnosis is inferred.
- Diagnoses are ranked by confidence:
  - Required symptoms contribute full weight.
  - Optional symptoms contribute half weight.

## 4. Testing and Validation
Tested with representative symptom sets:
- Cases that should match a single disease.
- Cases that should produce no diagnosis.
- Cases with overlapping symptoms.

Unit tests are provided in `tests/test_inference_engine.py`.

## 5. Limitations
- No laboratory results or patient history.
- No severity classification beyond confidence score.
- Limited to predefined diseases and symptoms.

## 6. Future Improvements
- Add negative rules (e.g., IF fever is absent, reduce probability of flu).
- Add larger disease database with external files.
- Add persistent case history and exportable diagnosis summaries.
- Integrate certainty factor or Bayesian reasoning.

## 7. Lessons Learned
- Clear rule structure improves explainability.
- Forward chaining is effective for symptom-to-diagnosis workflows.
- User input validation is important for reliable interaction.
