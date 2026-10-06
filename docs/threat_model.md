# Threat Model (what the questions defend against)

| Threat | Enabling exposures | Related categories |
|---|---|---|
| Account takeover (credential stuffing, phishing) | No MFA, reused passwords, weak recovery | MFA, Password reuse, Authentication, Login alerts |
| Social engineering / spear-phishing | Employer, family, travel, birthday details | Work/edu, Family, Birthday, Social-engineering |
| Impersonation / cloned profiles | Public friend lists, accepting strangers | Friends control, Unknown requests, Profile visibility |
| Physical safety / stalking | Location, check-ins, photo EXIF | Location, Photo metadata, Post visibility |
| Data leakage via apps | Over-permissioned third-party apps | Third-party access |
| Identity fraud | Full DOB, contact info, security-question facts | Birthday, Contact, Personal info |
| Long-term exposure | Old public posts | Historical posts |

Mapping idea for later: MITRE ATT&CK techniques T1566 (Phishing), T1078 (Valid Accounts), T1589 (Gather Victim Identity Information), T1598 (Phishing for Information).
