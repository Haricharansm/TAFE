
# TAFE AI Learning Assistant Prototype

This repository contains a Streamlit prototype for the proposed TAFE Learning & Development AI application.

It demonstrates three Phase 1 agents:

1. **Learner Assistant + AI Learning Coach**
   - Personalized course recommendations
   - Learner coaching chat
   - Manager/business head learning view
   - Role-aware access simulation

2. **Instructional Designer Agent**
   - Converts SME briefs into learning objectives
   - Generates module structure, storyboard outline, assessment questions and production notes
   - Simulates the content-pipeline support proposed for the L&D team

3. **Learning Campaigner Agent**
   - Generates personalized learning nudges
   - Supports campaigns such as World Book Day, birthdays, Farmer's Day and Safety Month
   - Uses mock HR + Moodle profile data

The app runs in deterministic mock mode by default. Azure OpenAI can be enabled through environment variables.

---

## Repository Structure

```text
tafe_learner_ai_coach_streamlit_prototype/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── .streamlit/
│   └── config.toml
└── data/
    ├── learners.csv
    ├── courses.csv
    ├── completions.csv
    └── campaigns.csv
```

---

## Run Locally

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

---

## Optional Azure OpenAI Setup

Copy `.env.example` to `.env` and set:

```bash
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_DEPLOYMENT=
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

Then load environment variables before running the app.

---

## Production Notes

For a real customer pilot, replace mock CSV files with:

- Moodle LMS connector for course catalog, enrolments and completion history
- HR system connector for employee profile, role, hierarchy and birthdays
- SharePoint connector for storyboards, QA artifacts and learning collateral
- Teams bot or embedded Moodle UI as the production experience
- Entra ID groups and row-level security for R&D confidentiality guardrails
- Azure AI Foundry / Azure OpenAI for agent orchestration
- Power BI semantic model for business-impact analytics

---

## Suggested GitHub Commands

```bash
git init
git add .
git commit -m "Initial TAFE AI learning assistant prototype"
git branch -M main
git remote add origin https://github.com/<org>/<repo>.git
git push -u origin main
```
