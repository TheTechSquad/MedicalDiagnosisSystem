"""Medical diagnosis expert system package."""

from .gui import run_gui
from .inference_engine import ForwardChainingEngine
from .knowledge_base import DISEASE_RULES, SYMPTOM_QUESTIONS

__all__ = [
    "run_gui",
    "ForwardChainingEngine",
    "DISEASE_RULES",
    "SYMPTOM_QUESTIONS",
]
