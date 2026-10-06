# Publish on GitHub and LinkedIn

## GitHub (beginner steps)
1. Create account at github.com; click **New repository**, name `social-media-privacy-risk-framework`, add description, keep Public, do NOT add README (you already have one).
2. In the project folder:
```bash
git init
git add .
git commit -m "Initial commit: Social Media Privacy Risk Assessment Framework"
git branch -M main
git remote add origin https://github.com/<your-username>/social-media-privacy-risk-framework.git
git push -u origin main
```
3. Replace `<YOUR NAME>` in `LICENSE`. Add repo topics: `cybersecurity`, `privacy`, `security-awareness`, `python`, `risk-assessment`.
4. Check the **Actions** tab - CI should turn green.
5. Add screenshots of `reports/dashboard.html` and a sample report to a `docs/img/` folder and link them in the README.
6. Pin the repo on your profile.

## Commit ideas (small, meaningful commits look professional)
`feat: question bank`, `feat: scoring engine`, `test: boundary tests`, `feat: synthetic generator`, `feat: HTML dashboard`, `docs: methodology`.

## LinkedIn post template
> I built the **Social Media Privacy Risk Assessment Framework** - a defensive, privacy-first tool that scores self-reported social-media settings (0-100) across 20 exposure categories, flags weaknesses, and generates prioritised recommendations and reports.
> - 40 questions, weighted scoring + compounding-risk rules
> - Synthetic-data dashboard (no real people, no scraping)
> - Python, unit-tested, CI on GitHub Actions
> Key learning: MFA + password reuse + oversharing combine to multiply risk. It is an educational framework, not a guarantee.
> Repo: <link>  #cybersecurity #privacy #python #infosec #securityawareness

## Resume bullet
Designed and built a Python privacy-risk assessment framework (20 categories, 40 weighted controls, compounding-risk model) with synthetic-data analytics dashboard, automated tests and CI.

## Interview talking points
Why higher = riskier; how weights were chosen and their limits; why no scraping (ethics/legal); how you validated scoring (monotonicity tests); how you would calibrate with real survey data.
