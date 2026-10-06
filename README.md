# 🛡️ Social Media Privacy Risk Assessment Framework

A **defensive, educational** cybersecurity project. A user answers questions about their own social-media privacy settings and habits; the framework returns a **Privacy Risk Score (0-100)**, a risk level, category scores, detected weaknesses, prioritised recommendations, a checklist, awareness guidance, and a shareable report.

> **Higher score = higher exposure / risk.**
> This is an educational risk framework, **not a guarantee** that an account will or will not be compromised.

## Risk levels
| Score | Level |
|---|---|
| 0-20 | LOW |
| 21-40 | MODERATE |
| 41-70 | HIGH |
| 71-100 | CRITICAL |

## Ethics (hard rules)
No scraping, no real-profile lookups, no account enumeration, no bypassing privacy settings, no tracking of individuals. Only **voluntarily entered answers** and **synthetic fictional profiles** (`DEMO-0001` ...). See [docs/ethics_and_scope.md](docs/ethics_and_scope.md).

## What it evaluates (20 categories, 40 questions)
Profile visibility · Personal info · Contact info · Location · Workplace/education · Birthday · Family/relationships · Post visibility · Friend/follower controls · Tagging · Third-party apps · Authentication · MFA · Password reuse · Login alerts · Unknown requests · Suspicious links/messages · Photo metadata · Historical posts · Social-engineering exposure

## Quick start (no installs needed for the core)
Requires Python 3.9+.
```bash
cd social-media-privacy-risk-framework
export PYTHONPATH=src            # Windows PowerShell:  $env:PYTHONPATH="src"

python -m smprf assess --report                # interactive questionnaire + saved report
python -m smprf demo --persona careless --report   # fictional persona (careless/average/aware/hardened)
python -m smprf file data/example_answers.json     # score answers from JSON
python -m smprf dashboard --n 200 --seed 42        # synthetic dataset + HTML dashboard -> reports/
python -m unittest discover -s tests -v            # run tests
```
Open `reports/dashboard.html` in your browser to see the aggregate dashboard.

### Optional web UI
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Project structure
```
src/smprf/questions.py   question bank, categories, weights, guidance
src/smprf/scoring.py     scoring engine, compounding rules, recommendations
src/smprf/synthetic.py   fictional profile generator
src/smprf/report.py      Markdown + HTML reports
src/smprf/dashboard.py   static HTML dashboard
src/smprf/cli.py         command-line interface
app.py                   optional Streamlit UI
tests/                   unit tests
docs/                    methodology, ethics, threat model, awareness, GitHub/LinkedIn guide
data/                    example answers + synthetic dataset
reports/                 sample generated reports and dashboard
```

## How scoring works (short)
Answer risk (0-4) → weighted category score → weighted overall base → capped compounding bonus (+15 max) for risky combinations (e.g. no MFA + reused passwords). Full detail and limitations: [docs/methodology.md](docs/methodology.md).

## Documentation
[Methodology](docs/methodology.md) · [Ethics & scope](docs/ethics_and_scope.md) · [Threat model](docs/threat_model.md) · [Awareness guide](docs/awareness_guide.md) · [GitHub & LinkedIn](docs/github_and_linkedin.md) · [Roadmap](docs/roadmap.md)

## License
MIT - see [LICENSE](LICENSE).
