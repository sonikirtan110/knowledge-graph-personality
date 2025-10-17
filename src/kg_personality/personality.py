"""Personality extraction utilities (simulated)
"""
from typing import Dict
import random

TRAITS = ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"]

class PersonalityEstimator:
    def __init__(self, seed: int = 42):
        random.seed(seed)

    def estimate_for_entities(self, entities) -> Dict[str, Dict[str, float]]:
        # entities is list of node ids
        out = {}
        for ent in entities:
            scores = {t: round(random.uniform(0, 1), 3) for t in TRAITS}
            out[ent] = scores
        return out
