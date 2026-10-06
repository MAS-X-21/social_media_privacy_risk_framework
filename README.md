# 🛡️ Social Media Privacy Risk Assessment Framework

A **defensive, educational cybersecurity project** designed to assess social-media privacy exposure based on a user's voluntarily provided privacy settings, security habits, and online behaviour.

The framework generates a **Privacy Risk Score (0–100)**, identifies the overall risk level, highlights potential weaknesses, provides prioritised recommendations, generates reports, and supports synthetic-data analysis.

> **Educational & Defensive Use Only:** This project does not scrape social-media platforms, access real accounts, collect credentials, track individuals, or bypass privacy controls.

---

## 📸 Project Screenshots

The `screenshots/` folder contains screenshots demonstrating the application's functionality, assessment process, results, reports, and dashboard.

### Application & Assessment

| Screenshot                                               | Description                           |
| -------------------------------------------------------- | ------------------------------------- |
| [Screenshot (62)](screenshots/Screenshot%20%2862%29.png) | Application interface / project start |
| [Screenshot (63)](screenshots/Screenshot%20%2863%29.png) | Privacy assessment interface          |
| [Screenshot (64)](screenshots/Screenshot%20%2864%29.png) | Assessment questions                  |
| [Screenshot (65)](screenshots/Screenshot%20%2865%29.png) | Assessment responses                  |
| [Screenshot (66)](screenshots/Screenshot%20%2866%29.png) | Assessment progression                |
| [Screenshot (67)](screenshots/Screenshot%20%2867%29.png) | Risk assessment results               |
| [Screenshot (68)](screenshots/Screenshot%20%2868%29.png) | Privacy Risk Score                    |
| [Screenshot (69)](screenshots/Screenshot%20%2869%29.png) | Risk category analysis                |
| [Screenshot (70)](screenshots/Screenshot%20%2870%29.png) | Detected privacy weaknesses           |
| [Screenshot (71)](screenshots/Screenshot%20%2871%29.png) | Prioritised recommendations           |
| [Screenshot (72)](screenshots/Screenshot%20%2872%29.png) | Privacy improvement checklist         |
| [Screenshot (73)](screenshots/Screenshot%20%2873%29.png) | Generated report                      |
| [Screenshot (74)](screenshots/Screenshot%20%2874%29.png) | Synthetic profile / demonstration     |
| [Screenshot (75)](screenshots/Screenshot%20%2875%29.png) | Dashboard / analytics                 |
| [Screenshot (76)](screenshots/Screenshot%20%2876%29.png) | Final project demonstration           |

> **Note:** The screenshots are included as visual proof of the project's functionality and development.

---

## 🎯 Project Objective

Social-media users often expose personal information without understanding the combined privacy risks created by their settings and online behaviour.

This framework provides an educational way to:

* Identify privacy weaknesses
* Estimate overall privacy exposure
* Understand risky security habits
* Prioritise improvements
* Increase cybersecurity awareness
* Demonstrate privacy-by-design concepts

The system is intended for **education, awareness, and defensive security analysis**.

---

## 🔐 Key Features

* 🔢 Privacy Risk Score from **0–100**
* 🚦 Risk-level classification
* 📊 Category-level risk analysis
* ⚠️ Weakness detection
* 🎯 Prioritised recommendations
* ✅ Privacy improvement checklist
* 📄 Markdown and HTML reports
* 📈 Synthetic-data dashboard
* 👤 Fictional demonstration personas
* 🧪 Automated unit tests
* 🖥️ Optional Streamlit web interface
* 🛡️ Defensive cybersecurity design
* 📚 Detailed methodology and threat-model documentation

---

## 📊 Risk Classification

|  Score | Risk Level  |
| -----: | ----------- |
|   0–20 | 🟢 LOW      |
|  21–40 | 🟡 MODERATE |
|  41–70 | 🟠 HIGH     |
| 71–100 | 🔴 CRITICAL |

**Higher score = higher estimated privacy exposure.**

The score is an educational assessment and should not be interpreted as a guarantee that an account will or will not be compromised.

---

## 🔎 Assessment Coverage

The framework evaluates **20 privacy and security categories across 40 questions**.

### Privacy Exposure

* Profile visibility
* Personal information
* Contact information
* Location exposure
* Workplace / education
* Birthday information
* Family / relationships
* Post visibility
* Friend / follower controls
* Tagging

### Security Exposure

* Third-party applications
* Authentication
* Multi-factor authentication
* Password reuse
* Login alerts
* Unknown requests
* Suspicious links and messages
* Photo metadata
* Historical posts
* Social-engineering exposure

---

## 🧮 How the Risk Score Works

The framework follows a structured scoring process:

```text
User Answer
     ↓
Risk Value (0–4)
     ↓
Category Score
     ↓
Weighted Overall Score
     ↓
Compounding Risk Rules
     ↓
Final Privacy Risk Score
     ↓
Risk Level + Recommendations
```

The scoring engine also applies limited compounding rules for combinations of risky behaviours, with the compounding bonus capped at **+15**.

For complete details, see:

* `docs/methodology.md`
* `docs/threat_model.md`
* `docs/ethics_and_scope.md`

---

## 🛡️ Ethics & Scope

This project follows a strict defensive cybersecurity approach.

### The framework DOES NOT:

* ❌ Scrape social-media platforms
* ❌ Search real user profiles
* ❌ Enumerate accounts
* ❌ Bypass privacy settings
* ❌ Track individuals
* ❌ Collect passwords or credentials
* ❌ Attempt account compromise
* ❌ Perform attacks against real users

### The framework DOES:

* ✅ Use voluntarily provided answers
* ✅ Use synthetic fictional profiles
* ✅ Provide privacy-awareness guidance
* ✅ Identify risky security practices
* ✅ Recommend defensive improvements

---

## 🧪 Demonstration Personas

The framework supports fictional demonstration personas such as:

```text
careless
average
aware
hardened
```

These personas are synthetic and are not associated with real social-media accounts.

---

## 🚀 Quick Start

### Requirements

* Python **3.9+**

### Clone the repository

```bash
git clone <repository-url>
cd social-media-privacy-risk-framework
```

### Set the Python path

#### Windows PowerShell

```powershell
$env:PYTHONPATH="src"
```

#### Linux / macOS

```bash
export PYTHONPATH=src
```

---

## ▶️ Run an Interactive Assessment

```bash
python -m smprf assess --report
```

This launches the interactive questionnaire and generates a report.

---

## 👤 Run a Synthetic Demonstration

```bash
python -m smprf demo --persona careless --report
```

Available fictional personas:

```text
careless
average
aware
hardened
```

---

## 📁 Score Answers from JSON

```bash
python -m smprf file data/example_answers.json
```

---

## 📈 Generate the Synthetic Dashboard

```bash
python -m smprf dashboard --n 200 --seed 42
```

The generated dashboard can be found inside:

```text
reports/
```

Open:

```text
reports/dashboard.html
```

in a web browser.

---

## 🖥️ Optional Streamlit Interface

Install the required packages:

```bash
pip install -r requirements.txt
```

Run:

```bash
streamlit run app.py
```

The Streamlit interface provides an interactive way to use the privacy assessment framework.

---

## 🧪 Run Tests

The project includes automated unit tests.

```bash
python -m unittest discover -s tests -v
```

Testing helps verify the scoring engine and core framework functionality.

---

## 📁 Project Structure

```text
social-media-privacy-risk-framework/
│
├── .github/
│   └── workflows/
│
├── data/
│   ├── example_answers.json
│   └── synthetic data
│
├── docs/
│   ├── methodology.md
│   ├── ethics_and_scope.md
│   ├── threat_model.md
│   ├── awareness_guide.md
│   ├── github_linkedin.md
│   └── roadmap.md
│
├── reports/
│   ├── sample reports
│   └── dashboard.html
│
├── screenshots/
│   ├── Screenshot (62).png
│   ├── Screenshot (63).png
│   ├── Screenshot (64).png
│   ├── Screenshot (65).png
│   ├── Screenshot (66).png
│   ├── Screenshot (67).png
│   ├── Screenshot (68).png
│   ├── Screenshot (69).png
│   ├── Screenshot (70).png
│   ├── Screenshot (71).png
│   ├── Screenshot (72).png
│   ├── Screenshot (73).png
│   ├── Screenshot (74).png
│   ├── Screenshot (75).png
│   └── Screenshot (76).png
│
├── src/
│   └── smprf/
│       ├── questions.py
│       ├── scoring.py
│       ├── synthetic.py
│       ├── report.py
│       ├── dashboard.py
│       └── cli.py
│
├── tests/
│
├── app.py
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

---

## 🛠️ Technology Stack

| Technology | Purpose                                       |
| ---------- | --------------------------------------------- |
| Python     | Core framework and scoring engine             |
| Streamlit  | Interactive web interface                     |
| HTML       | Reports and dashboard                         |
| JSON       | Example and assessment data                   |
| unittest   | Automated testing                             |
| Git        | Version control                               |
| GitHub     | Source-code hosting and project documentation |

---

## 🧩 Core Components

### `questions.py`

Contains:

* Question bank
* Privacy categories
* Risk weights
* Guidance information

### `scoring.py`

Responsible for:

* Risk calculations
* Category scoring
* Overall score
* Compounding rules
* Recommendations

### `synthetic.py`

Generates fictional demonstration profiles and synthetic datasets.

### `report.py`

Generates Markdown and HTML reports.

### `dashboard.py`

Creates a static HTML dashboard from synthetic data.

### `cli.py`

Provides the command-line interface for running assessments and demonstrations.

---

## 📚 Documentation

Detailed project documentation is available in the `docs/` directory:

* **Methodology** — scoring model and calculations
* **Ethics & Scope** — defensive-use boundaries
* **Threat Model** — identified privacy threats
* **Awareness Guide** — practical privacy guidance
* **GitHub & LinkedIn Guide** — project presentation guidance
* **Roadmap** — future improvements

---

## 🎓 Learning Outcomes

This project demonstrates practical understanding of:

* Cybersecurity fundamentals
* Privacy risk assessment
* Security awareness
* Risk scoring methodologies
* Social-engineering risks
* Defensive security
* Python development
* Data analysis
* Automated testing
* Technical documentation
* Git and GitHub workflow

---

## 🔮 Future Improvements

Potential future enhancements include:

* Additional privacy assessment categories
* More advanced risk modelling
* Improved dashboard visualisations
* Exportable PDF reports
* Configurable scoring profiles
* Additional synthetic datasets
* Security-awareness recommendations based on user risk patterns

---

## ⚠️ Disclaimer

This project is intended **solely for educational and defensive cybersecurity purposes**.

The Privacy Risk Score represents an estimate based on user-provided answers and predefined risk rules. It does not guarantee that an account is secure or insecure and does not predict whether an account will be compromised.

---

## 📄 License

This project is released under the **MIT License**.

---

## 👨‍💻 Project

**Social Media Privacy Risk Assessment Framework**

A defensive cybersecurity project focused on **social-media privacy awareness, risk assessment, and security education**.
