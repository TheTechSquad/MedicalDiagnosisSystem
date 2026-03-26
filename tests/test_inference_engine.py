import unittest

from medical_expert.inference_engine import ForwardChainingEngine
from medical_expert.knowledge_base import DISEASE_RULES


class TestForwardChainingEngine(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = ForwardChainingEngine(DISEASE_RULES)

    def test_common_cold_diagnosis(self) -> None:
        symptoms = {
            "cough": True,
            "sore_throat": True,
            "runny_nose": True,
            "sneezing": True,
            "headache": False,
        }
        results = self.engine.diagnose(symptoms)
        diseases = [item.disease for item in results]
        self.assertIn("Common Cold", diseases)

    def test_flu_diagnosis(self) -> None:
        symptoms = {
            "fever": True,
            "body_ache": True,
            "fatigue": True,
            "dry_cough": True,
            "headache": True,
        }
        results = self.engine.diagnose(symptoms)
        self.assertEqual(results[0].disease, "Influenza (Flu)")

    def test_covid_diagnosis(self) -> None:
        symptoms = {
            "fever": True,
            "dry_cough": True,
            "fatigue": True,
            "loss_of_taste_smell": True,
        }
        results = self.engine.diagnose(symptoms)
        diseases = [item.disease for item in results]
        self.assertIn("COVID-19 (Mild Pattern)", diseases)

    def test_no_match(self) -> None:
        symptoms = {
            "itchy_eyes": True,
            "abdominal_cramps": True,
        }
        results = self.engine.diagnose(symptoms)
        self.assertEqual(results, [])


if __name__ == "__main__":
    unittest.main()
