import os
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv

try:
    from openai import AzureOpenAI
except Exception:
    AzureOpenAI = None

load_dotenv()

APP_DIR = Path(__file__).parent
DATA_DIR = APP_DIR / "data"

st.set_page_config(
    page_title="TAFE AI Opportunity Assessment",
    page_icon="🚜",
    layout="wide",
    initial_sidebar_state="expanded",
)

VALUE_SCORE = {"Low": 1, "Medium": 2, "Medium-High": 3, "High": 4}
EFFORT_SCORE = {"Low": 1, "Medium": 2, "Medium-High": 3, "High": 4}


def load_data():
    use_cases = pd.read_csv(DATA_DIR / "use_cases.csv")
    challenges = pd.read_csv(DATA_DIR / "challenges.csv")
    architecture = pd.read_csv(DATA_DIR / "architecture.csv")
    use_cases["value_score"] = use_cases["value"].map(VALUE_SCORE)
    use_cases["effort_score"] = use_cases["effort"].map(EFFORT_SCORE)
    return use_cases, challenges, architecture


def metric_card(label, value, help_text=None):
    st.metric(label=label, value=value, help=help_text)


def render_header():
    st.title("TAFE AI Opportunity Assessment")
    st.caption("Interactive Streamlit app for Learning & Development AI transformation planning")


def render_sidebar():
    st.sidebar.title("Navigation")
    section = st.sidebar.radio(
        "Go to",
        [
            "Executive Summary",
            "Challenges",
            "Use Case Portfolio",
            "Roadmap",
            "Architecture",
            "AI Assistant",
        ],
    )
    st.sidebar.divider()
    st.sidebar.markdown("**Strategic pillars**")
    st.sidebar.write("Learning adoption")
    st.sidebar.write("Learning experience")
    st.sidebar.write("Business impact")
    return section


def executive_summary(use_cases):
    render_header()
    st.subheader("Recommended approach")
    st.info(
        "Lead with the flagship Learner Assistant + AI Learning Coach as the Phase 1 strategic POC, "
        "while running quick-win agents for Instructional Design and Learning Campaigns in parallel. "
        "This creates visible team productivity wins while building the data and orchestration foundation."
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Employees served", "4,200", "Approximate internal learner population")
    with c2:
        metric_card("Prioritized use cases", len(use_cases))
    with c3:
        metric_card("Phase 1 horizon", "0–3 months")
    with c4:
        metric_card("Core platform", "Azure + Teams")

    st.subheader("Phase 1 focus")
    phase1 = use_cases[use_cases["phase"].str.contains("Phase 1", na=False)]
    st.dataframe(
        phase1[["id", "name", "bucket", "value", "effort", "timeline", "kpi"]],
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("Portfolio snapshot")
    bucket_counts = use_cases.groupby("bucket", as_index=False).size()
    fig = px.bar(bucket_counts, x="bucket", y="size", text="size", title="Use cases by prioritization bucket")
    st.plotly_chart(fig, use_container_width=True)


def challenges_page(challenges):
    render_header()
    st.subheader("Current-state challenges")
    for _, row in challenges.iterrows():
        with st.container(border=True):
            st.markdown(f"### {row['challenge']}")
            st.write(row["description"])


def portfolio_page(use_cases):
    render_header()
    st.subheader("AI use case portfolio")

    fig = px.scatter(
        use_cases,
        x="effort_score",
        y="value_score",
        text="id",
        hover_name="name",
        hover_data=["bucket", "timeline", "kpi"],
        title="Value vs Effort Matrix",
        labels={"effort_score": "Effort", "value_score": "Value"},
        range_x=[0.5, 4.5],
        range_y=[0.5, 4.5],
    )
    fig.update_traces(textposition="top center", marker=dict(size=18))
    fig.update_xaxes(tickvals=[1, 2, 3, 4], ticktext=["Low", "Medium", "Medium-High", "High"])
    fig.update_yaxes(tickvals=[1, 2, 3, 4], ticktext=["Low", "Medium", "Medium-High", "High"])
    st.plotly_chart(fig, use_container_width=True)

    selected = st.selectbox("Select a use case", use_cases["name"].tolist())
    row = use_cases[use_cases["name"] == selected].iloc[0]
    c1, c2, c3 = st.columns(3)
    with c1:
        metric_card("Value", row["value"])
    with c2:
        metric_card("Effort", row["effort"])
    with c3:
        metric_card("Timeline", row["timeline"])
    st.markdown(f"**Bucket:** {row['bucket']}")
    st.markdown(f"**Phase:** {row['phase']}")
    st.markdown(f"**Primary KPI:** {row['kpi']}")

    st.subheader("Full use case table")
    st.dataframe(
        use_cases[["id", "name", "bucket", "value", "effort", "timeline", "kpi", "phase"]],
        use_container_width=True,
        hide_index=True,
    )


def roadmap_page(use_cases):
    render_header()
    st.subheader("Indicative roadmap")

    phases = {
        "Phase 1 — Foundation & Quick Wins (Months 0–3)": ["UC-4", "UC-1", "UC-3"],
        "Phase 2 — Scale & Expand (Months 3–6)": ["UC-2", "UC-6"],
        "Phase 3 — Strategic Transformation (Months 6–12)": ["UC-5", "UC-6", "UC-7"],
    }

    for phase, ids in phases.items():
        st.markdown(f"### {phase}")
        phase_df = use_cases[use_cases["id"].isin(ids)]
        cols = st.columns(len(phase_df))
        for col, (_, row) in zip(cols, phase_df.iterrows()):
            with col:
                with st.container(border=True):
                    st.markdown(f"**{row['id']} — {row['name']}**")
                    st.caption(f"{row['bucket']} | Value: {row['value']} | Effort: {row['effort']}")
                    st.write(row["timeline"])
                    st.write(row["kpi"])


def architecture_page(architecture):
    render_header()
    st.subheader("Recommended Microsoft-centric architecture")
    st.dataframe(architecture, use_container_width=True, hide_index=True)

    st.markdown("### Reference flow")
    st.code(
        """
Moodle + HR + SharePoint
        ↓
Hybrid connectors / ingestion
        ↓
Curated Azure data layer
        ↓
Azure AI Foundry + Saxon (AI)ssist orchestrator
        ↓
Role-aware sub-agents: Learner Coach, Instructional Designer, QA Reviewer, Campaigner, PM, Analytics
        ↓
Microsoft Teams / Moodle embedded experience
        ↓
Power BI dashboards + business-impact insights
        """.strip(),
        language="text",
    )


def build_context(use_cases, challenges, architecture):
    return f"""
You are an AI assistant for TAFE Learning & Development AI Opportunity Assessment.
The assessment recommends a Microsoft-centric Azure-first multi-agent architecture using Azure AI Foundry,
Microsoft Teams, Moodle hybrid connectors, SharePoint, Power Automate, Power BI and Entra ID guardrails.

Strategic pillars: learning adoption, learning experience, business impact.

Challenges:
{challenges.to_string(index=False)}

Use cases:
{use_cases[['id','name','bucket','value','effort','timeline','kpi','phase']].to_string(index=False)}

Architecture:
{architecture.to_string(index=False)}
"""


def call_azure_openai(prompt, context):
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview")
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

    if not all([endpoint, api_key, deployment]) or AzureOpenAI is None:
        return None

    client = AzureOpenAI(api_key=api_key, azure_endpoint=endpoint, api_version=api_version)
    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": "Answer as a concise enterprise AI consultant. Use only the provided context."},
            {"role": "user", "content": context},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content


def ai_assistant_page(use_cases, challenges, architecture):
    render_header()
    st.subheader("AI Assistant")
    st.write("Ask questions about the TAFE AI opportunity portfolio, roadmap, KPIs or architecture.")

    context = build_context(use_cases, challenges, architecture)
    prompt = st.text_area("Question", placeholder="Example: What should we build first and why?")

    if st.button("Ask"):
        if not prompt.strip():
            st.warning("Please enter a question.")
            return
        answer = call_azure_openai(prompt, context)
        if answer:
            st.success(answer)
        else:
            st.warning(
                "Azure OpenAI is not configured. Add AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, "
                "AZURE_OPENAI_API_VERSION and AZURE_OPENAI_DEPLOYMENT to your .env or Streamlit secrets."
            )
            st.markdown("**Local context available to the assistant:**")
            st.code(context[:4000], language="text")


def main():
    use_cases, challenges, architecture = load_data()
    section = render_sidebar()

    if section == "Executive Summary":
        executive_summary(use_cases)
    elif section == "Challenges":
        challenges_page(challenges)
    elif section == "Use Case Portfolio":
        portfolio_page(use_cases)
    elif section == "Roadmap":
        roadmap_page(use_cases)
    elif section == "Architecture":
        architecture_page(architecture)
    elif section == "AI Assistant":
        ai_assistant_page(use_cases, challenges, architecture)


if __name__ == "__main__":
    main()
