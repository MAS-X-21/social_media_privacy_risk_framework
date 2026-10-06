# Ethics and Scope

## In scope
- Self-assessment of the user's OWN privacy configuration via a questionnaire.
- Synthetic, fictional personas (`DEMO-xxxx`) for dashboards and testing.
- Defensive guidance and awareness training.

## Out of scope (never implemented)
- Scraping social-media sites or calling platform APIs against real profiles
- Collecting data about real people, or identifying/profiling/tracking individuals
- Bypassing privacy settings, accessing private accounts, account enumeration
- Storing credentials, tokens, or real personal data

## Design choices that enforce this
- No network code and no third-party runtime dependencies in the core.
- No persistence: answers live in memory unless the user saves a report.
- Reports show *categories of exposure*, never real identifiers.
- Synthetic data generated from a random seed.

## Disclaimer
Educational risk framework. It is not a guarantee that an account will or will not be compromised.
