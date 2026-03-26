# Knowledge Base Documentation

## Knowledge Representation Approach
The system uses production rules in the form:

**IF** required symptom set is true **THEN** infer disease diagnosis.

Each disease contains:
- Required symptoms: must be present to trigger inference.
- Optional symptoms: increase confidence score but are not mandatory.
- Explanation: reasoning text shown to the user.

## Disease Rules

### 1) Common Cold
- Required: cough, sore_throat, runny_nose, sneezing
- Optional: headache, fatigue

### 2) Influenza (Flu)
- Required: fever, body_ache, fatigue, dry_cough
- Optional: headache, sore_throat

### 3) Allergic Rhinitis
- Required: sneezing, itchy_eyes, runny_nose, nasal_congestion
- Optional: cough

### 4) COVID-19 (Mild Pattern)
- Required: fever, dry_cough, fatigue, loss_of_taste_smell
- Optional: sore_throat, headache

### 5) Strep Throat
- Required: sore_throat, fever, swollen_lymph_nodes, painful_swallowing
- Optional: headache

### 6) Gastroenteritis
- Required: nausea, vomiting, diarrhea, abdominal_cramps
- Optional: fever, fatigue

## Conflict Handling
Multiple rules can fire if their conditions are satisfied. Diagnoses are sorted by confidence.
