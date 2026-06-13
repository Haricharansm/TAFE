# TAFE AIssist — L&D AI Platform Prototype

> **Prototype built by Saxon** · Based on the AI Opportunity Assessment Workshop with TAFE Learning & Development · May 2026

A multi-agent AI prototype demonstrating three Phase 1 use cases from Saxon's AI Opportunity Assessment for TAFE (Tractors and Farm Equipment). Built with Streamlit, styled in TAFE's brand palette, and grounded in the real workflows, role gaps, and system landscape identified during the workshop.

---

## Agents Included

### 🎓 UC-4 · Learner Assistant + AI Coach *(Strategic POC — Phase 1 Flagship)*
Role-aware conversational agent surfacing the right experience based on who's asking:
- **Learner view** — personalised course recommendations, skill gap analysis, AI coaching chat, overdue alerts
- **Manager view** — team completion heatmap, at-risk learner identification, one-click nudge to flagged team members
- **Leadership view** — conversational analytics engine, function-level heatmap, NPI readiness tracking, R&D confidential access gating

### ✏️ UC-1 · Instructional Designer Agent *(Quick Win — Phase 1)*
AI agent that fills the instructional design role gap in TAFE's content pipeline:
- Accepts a content brief (module title, audience, format)
- Generates a full storyboard: module sequence, narration/interaction design, asset requirements, timing
- Built-in QA pre-check across Visual Consistency, Instructional Integrity, Accessibility, and Technical dimensions
- Flags WCAG accessibility issues and surfaces ID notes before handoff to the media team

### 📣 UC-3 · Learning Campaigner Agent *(Quick Win — Phase 1)*
AI agent that runs TAFE's learning campaigns consistently — something the current facilitation-heavy team cannot sustain manually:
- Campaign dashboard: Birthday Nudge Engine, World Book Day, Farmer's Day, Diwali, and more
- Live performance metrics per campaign (nudges sent, open rate, learning start rate)
- Nudge Builder: regenerate personalised messages by tone and length
- Real-time Birthday Queue showing today's employees with recommended course and delivery status

---

## Technology Context

This prototype simulates the recommended platform architecture from the Saxon AI Opportunity Assessment:

| Layer | Platform |
|---|---|
| AI Compute | Azure AI Foundry (GPT-4 class + multimodal) |
| Multi-agent orchestration | Saxon AIssist accelerator on Azure |
| User interface | Microsoft Teams (primary) + Moodle web portal |
| Data foundation | Azure Data Lake + on-prem Moodle (hybrid connectors) |
| Identity & guardrails | Microsoft Entra ID (3-layer guardrail design) |
| Workflow automation | Power Automate |
| Analytics & BI | Power BI semantic model |

---

## Running Locally

**Prerequisites:** Python 3.9 or higher

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/tafe-aissist.git
cd tafe-aissist

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run tafe_aissist.py
```

The app opens automatically at `http://localhost:8501`

---

## Deploying to Streamlit Community Cloud (Free Hosting)

1. Push this repository to GitHub (public or private)
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub
3. Click **New app** → select this repo → set main file to `tafe_aissist.py`
4. Click **Deploy** — you'll have a shareable URL in ~2 minutes

The deployed URL can be shared directly with the TAFE L&D team for review, no installation required.

---

## Repository Structure

```
tafe-aissist/
├── tafe_aissist.py       # Main Streamlit application
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

---

## Governance & Responsible AI

This prototype reflects the five-pillar governance framework agreed during the workshop:

- **Human-in-the-loop** — AI agents draft and recommend; humans approve before any action
- **Audit trail** — every AI output carries model, prompt, timestamp, and approver metadata
- **Data residency** — all TAFE data stays within TAFE's Azure tenant; no public model training
- **Validation-first** — agents achieve ≥90% accuracy against human benchmark before deployment
- **Transparent limitations** — outputs include source citations and confidence indicators

R&D / NPI content is gated through a dedicated sub-agent with admin-controlled access classes, implementing a three-layer guardrail design (Teams access → in-prompt role check → database row security).

---

## About Saxon

Saxon is a Microsoft-exclusive solutions partner with deep expertise in Azure AI, enterprise platform delivery, and agentic AI deployments. This prototype mirrors the Riddell RIA reference architecture (deployed on Microsoft Azure) demonstrated during the TAFE workshop.

---

*Saxon Confidential · Prototype · May 2026*
