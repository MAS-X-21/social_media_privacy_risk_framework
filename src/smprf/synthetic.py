"""Synthetic (fictional) profile generator.

Profiles are random answer sets with persona-based risk tendencies.
They represent NO real person. Identifiers look like DEMO-0001.
"""
import csv
import random
from typing import Dict, List
from .questions import QUESTIONS, CATEGORIES
from .scoring import assess

PERSONAS = {            # persona -> (mean risk, spread)
    "careless":   (3.0, 0.8),
    "average":    (2.0, 0.9),
    "aware":      (1.0, 0.7),
    "hardened":   (0.3, 0.4),
}
PERSONA_WEIGHTS = {"careless": 0.2, "average": 0.45, "aware": 0.25, "hardened": 0.10}

def synthetic_answers(persona: str, rng: random.Random) -> Dict[str, int]:
    mean, sd = PERSONAS[persona]
    answers = {}
    for q in QUESTIONS:
        target = max(0.0, min(4.0, rng.gauss(mean, sd)))
        best = min(range(len(q.options)), key=lambda i: (abs(q.options[i][1] - target), rng.random()))
        answers[q.id] = best
    return answers

def generate_profiles(n: int = 200, seed: int = 42) -> List[dict]:
    rng = random.Random(seed)
    names, weights = zip(*PERSONA_WEIGHTS.items())
    rows = []
    for i in range(1, n + 1):
        persona = rng.choices(names, weights)[0]
        a = synthetic_answers(persona, rng)
        res = assess(a)
        row = {"profile_id": f"DEMO-{i:04d}", "persona": persona, "score": res.overall, "level": res.level}
        for c in CATEGORIES:
            row[c.key] = res.category_scores[c.key]
        rows.append(row)
    return rows

def write_csv(rows: List[dict], path: str) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
