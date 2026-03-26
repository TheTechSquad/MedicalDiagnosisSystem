from medical_expert.models import DiseaseRule


# Standardized symptom prompts used by the GUI layer.
SYMPTOM_QUESTIONS = {
    "fever": "Do you have fever?",
    "cough": "Do you have cough?",
    "dry_cough": "Do you have dry cough?",
    "sore_throat": "Do you have sore throat?",
    "runny_nose": "Do you have runny nose?",
    "sneezing": "Do you have frequent sneezing?",
    "body_ache": "Do you have body aches?",
    "fatigue": "Do you feel unusual fatigue?",
    "headache": "Do you have headache?",
    "itchy_eyes": "Do you have itchy eyes?",
    "nasal_congestion": "Do you have nasal congestion?",
    "loss_of_taste_smell": "Did you lose taste or smell recently?",
    "swollen_lymph_nodes": "Do you have swollen lymph nodes in the neck?",
    "painful_swallowing": "Is swallowing painful?",
    "nausea": "Do you feel nausea?",
    "vomiting": "Do you have vomiting?",
    "diarrhea": "Do you have diarrhea?",
    "abdominal_cramps": "Do you have abdominal cramps?",
}


# Production rules: IF all required symptoms are present THEN infer disease.
DISEASE_RULES = [
    DiseaseRule(
        disease="Common Cold",
        required_symptoms={"cough", "sore_throat", "runny_nose", "sneezing"},
        optional_symptoms={"headache", "fatigue"},
        explanation="Typical upper-respiratory symptoms suggest common cold.",
    ),
    DiseaseRule(
        disease="Influenza (Flu)",
        required_symptoms={"fever", "body_ache", "fatigue", "dry_cough"},
        optional_symptoms={"headache", "sore_throat"},
        explanation="High fever with body ache and fatigue strongly indicates flu.",
    ),
    DiseaseRule(
        disease="Allergic Rhinitis",
        required_symptoms={"sneezing", "itchy_eyes", "runny_nose", "nasal_congestion"},
        optional_symptoms={"cough"},
        explanation="Sneezing with itchy eyes and nasal symptoms is common in allergies.",
    ),
    DiseaseRule(
        disease="COVID-19 (Mild Pattern)",
        required_symptoms={"fever", "dry_cough", "fatigue", "loss_of_taste_smell"},
        optional_symptoms={"sore_throat", "headache"},
        explanation="Loss of taste/smell with fever and dry cough suggests COVID-19.",
    ),
    DiseaseRule(
        disease="Strep Throat",
        required_symptoms={"sore_throat", "fever", "swollen_lymph_nodes", "painful_swallowing"},
        optional_symptoms={"headache"},
        explanation="Severe sore throat with fever and neck nodes is consistent with strep throat.",
    ),
    DiseaseRule(
        disease="Gastroenteritis",
        required_symptoms={"nausea", "vomiting", "diarrhea", "abdominal_cramps"},
        optional_symptoms={"fever", "fatigue"},
        explanation="Acute digestive symptoms indicate likely gastroenteritis.",
    ),
]
