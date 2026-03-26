# Medical Diagnosis Expert System (Project 2)

A Python rule-based expert system for diagnosing common medical conditions from symptoms using forward chaining.

## Implemented Diseases
- Common Cold
- Influenza (Flu)
- Allergic Rhinitis
- COVID-19 (Mild Pattern)
- Strep Throat
- Gastroenteritis

## Features
- Rule-based knowledge base with required and optional symptoms.
- Forward chaining inference engine.
- Graphical user interface (Tkinter) for symptom selection and diagnosis display.
- Ranked diagnosis output with confidence percentages and reasoning.
- Unit tests for core inference behavior.

## Run the System (GUI)
1. Open terminal in the project root.
2. Run:

```bash
python main.py
```

## Run Tests
```bash
python -m unittest discover -s tests
```

## Disclaimer
This system is for educational use only and does not provide medical advice.
