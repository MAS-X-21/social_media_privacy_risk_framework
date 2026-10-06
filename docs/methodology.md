# Scoring Methodology

**Direction:** higher score = higher privacy exposure / risk.

| Score | Level |
|---|---|
| 0-20 | LOW |
| 21-40 | MODERATE |
| 41-70 | HIGH |
| 71-100 | CRITICAL |

## Steps
1. **Question risk (0-4).** Every answer option carries a risk value; 0 = best practice, 4 = worst.
2. **Category score** = `100 x sum(question_weight x risk) / sum(question_weight x 4)`.
3. **Base score** = weighted average of the 20 category scores. Category weights (3-7) reflect how directly a category enables account takeover or social engineering (e.g. MFA = 7, tagging = 4, login alerts = 3).
4. **Compounding rules** add a bonus when risky behaviours combine (capped at +15 total):
   - R1 +6 No effective MFA AND password reuse
   - R2 +4 Public profile AND visible contact info AND urgency-trusting behaviour
   - R3 +3 Frequent location sharing AND public family details
   - R4 +3 Accepting strangers AND public friend list
   - R5 +3 Unprotected recovery email AND no login alerts
5. **Final** = clamp(round(base + bonus), 0, 100), mapped to the level table.

## Weaknesses and recommendations
- A **weakness** is raised when an answer has risk >= 3. Severity: *Critical* (risk 4, question weight 3), *High* (risk 4), *Medium* (risk 3).
- A **recommendation** is raised when risk >= 2, ranked by `question_weight x risk`. Top 3 = "Do now", next 5 = "Do this week", rest = "Do this month".
- **Checklist** items are ticked when the category score <= 25.

## Limitations (be honest in interviews)
- Weights are expert-judgement heuristics, not empirically calibrated on breach data.
- Answers are self-reported and may be inaccurate.
- Platform settings differ; questions are platform-agnostic.
- The score is educational, not a guarantee about any account.

## Validation performed
Unit tests check: best answers => 0/LOW, worst => 100/CRITICAL, band boundaries, monotonicity (making an answer worse never lowers the score), bonus cap, input validation, deterministic synthetic data, and persona ordering.
