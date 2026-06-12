# TAFE AI Opportunity Assessment - Streamlit App

A GitHub-ready Streamlit application that converts the TAFE Learning & Development AI Opportunity Assessment into an interactive executive dashboard.

## What this app shows

- Executive summary and strategic recommendation
- Current state challenges
- AI use case portfolio with value/effort scoring
- Roadmap by phase
- Microsoft-centric Azure architecture
- Optional AI assistant using Azure OpenAI

## Quick start

```bash
git clone <your-repo-url>
cd tafe_ai_streamlit_app
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Optional Azure OpenAI setup

Create a `.env` file:

```bash
AZURE_OPENAI_ENDPOINT=https://<your-resource>.openai.azure.com/
AZURE_OPENAI_API_KEY=<your-key>
AZURE_OPENAI_API_VERSION=2024-08-01-preview
AZURE_OPENAI_DEPLOYMENT=<your-model-deployment-name>
```

The app will run without Azure OpenAI. The assistant tab will show a setup message until these values are provided.

## Suggested GitHub workflow

```bash
git init
git add .
git commit -m "Initial TAFE AI Streamlit app"
git branch -M main
git remote add origin https://github.com/<org>/<repo>.git
git push -u origin main
```

## Deployment options

- Streamlit Community Cloud for demo use
- Azure App Service for enterprise deployment
- Azure Container Apps if containerization is preferred
