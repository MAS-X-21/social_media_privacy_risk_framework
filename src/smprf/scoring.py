"""Scoring engine. HIGHER score = HIGHER privacy exposure / risk.

Method (see docs/methodology.md):
  1. Each answer has a risk value 0 (best) .. 4 (worst).
  2. Category score  = 100 * sum(q_weight * risk) / sum(q_weight * 4)
  3. Base score      = weighted average of category scores (category weights)
  4. Compounding rules add a small bonus when risky behaviours combine
     (e.g. no MFA AND reused passwords). Total bonus is capped at +15.
  5. Final score is clamped to 0..100 and mapped to a risk level.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Tuple
from .questions import CATEGORIES, CATEGORY_BY_KEY, QUESTIONS, QUESTION_BY_ID

DISCLAIMER = ("This is an EDUCATIONAL risk framework based on self-reported answers. "
              "It estimates privacy exposure; it is NOT a guarantee that an account "
              "will or will not be compromised, and it is not a penetration test or audit.")

LEVELS = [(20, "LOW"), (40, "MODERATE"), (70, "HIGH"), (100, "CRITICAL")]
MAX_BONUS = 15.0

def risk_level(score: float) -> str:
    s = round(score)
    for upper, name in LEVELS:
        if s <= upper:
            return name
    return "CRITICAL"

def _risk(answers: Dict[str, int], qid: str) -> int:
    """Risk value (0-4) of an answered question, or -1 if unanswered."""
    if qid not in answers:
        return -1
    return QUESTION_BY_ID[qid].options[answers[qid]][1]

# (rule id, title, explanation, bonus, predicate on answers)
def _rules():
    r = _risk
    return [
     ("R1", "Account-takeover chain", "No effective MFA combined with reused passwords makes breach-driven takeover much easier.", 6.0,
      lambda a: r(a,"mf1") >= 3 and r(a,"pr1") >= 3),
     ("R2", "Targeted-scam readiness", "A public profile, visible contact details and urgency-driven trust form a strong scam setup.", 4.0,
      lambda a: r(a,"pv1") >= 3 and (r(a,"ci1") >= 3 or r(a,"ci2") >= 3) and r(a,"se1") >= 3),
     ("R3", "Routine and family exposure", "Frequent location sharing plus public family details reveals patterns about you and others.", 3.0,
      lambda a: r(a,"lo1") >= 3 and r(a,"fa2") >= 3),
     ("R4", "Clone-and-contact risk", "Accepting strangers while your friend list is public eases account cloning and contact targeting.", 3.0,
      lambda a: r(a,"ur1") >= 3 and r(a,"fr2") >= 3),
     ("R5", "Weak recovery path", "Unprotected recovery email plus no login alerts means takeover could go unnoticed.", 3.0,
      lambda a: r(a,"mf2") >= 4 and r(a,"la1") >= 3),
    ]

@dataclass
class Assessment:
    overall: int
    level: str
    base_score: float
    bonus: float
    category_scores: Dict[str, float]
    adjustments: List[Dict]
    weaknesses: List[Dict]
    recommendations: List[Dict]
    checklist: List[Dict]
    awareness: List[Dict]
    answered: int
    total_questions: int
    disclaimer: str = DISCLAIMER

    def to_dict(self):
        return self.__dict__.copy()

def validate_answers(answers: Dict[str, int]) -> None:
    for qid, idx in answers.items():
        if qid not in QUESTION_BY_ID:
            raise ValueError(f"Unknown question id: {qid}")
        n = len(QUESTION_BY_ID[qid].options)
        if not isinstance(idx, int) or isinstance(idx, bool) or not 0 <= idx < n:
            raise ValueError(f"Answer for {qid} must be an integer 0..{n-1}, got {idx!r}")

def category_score(answers: Dict[str, int], key: str):
    num = den = 0
    for q in QUESTIONS:
        if q.category != key or q.id not in answers:
            continue
        num += q.weight * q.options[answers[q.id]][1]
        den += q.weight * 4
    return None if den == 0 else 100.0 * num / den

def assess(answers: Dict[str, int]) -> Assessment:
    validate_answers(answers)
    if not answers:
        raise ValueError("No answers provided.")
    cat_scores: Dict[str, float] = {}
    num = den = 0.0
    for c in CATEGORIES:
        s = category_score(answers, c.key)
        if s is None:
            continue
        cat_scores[c.key] = round(s, 1)
        num += c.weight * s
        den += c.weight
    base = num / den
    adjustments, bonus = [], 0.0
    for rid, title, why, pts, pred in _rules():
        if pred(answers):
            adjustments.append({"id": rid, "title": title, "explanation": why, "points": pts})
            bonus += pts
    bonus = min(bonus, MAX_BONUS)
    overall = int(round(max(0.0, min(100.0, base + bonus))))

    weaknesses, recs = [], []
    for q in QUESTIONS:
        if q.id not in answers:
            continue
        label, risk = q.options[answers[q.id]]
        cat = CATEGORY_BY_KEY[q.category].name
        if risk >= 3:
            sev = "Critical" if (risk == 4 and q.weight >= 3) else ("High" if risk == 4 else "Medium")
            weaknesses.append({"question_id": q.id, "category": cat, "finding": q.weakness,
                               "your_answer": label, "severity": sev})
        if risk >= 2:
            recs.append({"question_id": q.id, "category": cat, "action": q.recommendation,
                         "priority_score": q.weight * risk})
    order = {"Critical": 0, "High": 1, "Medium": 2}
    weaknesses.sort(key=lambda w: (order[w["severity"]], w["category"]))
    recs.sort(key=lambda x: -x["priority_score"])
    for i, rc in enumerate(recs, 1):
        rc["rank"] = i
        rc["priority"] = "Do now" if i <= 3 else ("Do this week" if i <= 8 else "Do this month")

    checklist = []
    for c in CATEGORIES:
        if c.key in cat_scores:
            checklist.append({"category": c.name, "item": c.checklist, "done": cat_scores[c.key] <= 25})
    worst = sorted(cat_scores, key=lambda k: -cat_scores[k])[:5]
    awareness = [{"category": CATEGORY_BY_KEY[k].name, "score": cat_scores[k],
                  "guidance": CATEGORY_BY_KEY[k].awareness} for k in worst if cat_scores[k] > 25]
    return Assessment(overall, risk_level(overall), round(base, 1), bonus, cat_scores,
                      adjustments, weaknesses, recs, checklist, awareness,
                      len(answers), len(QUESTIONS))
