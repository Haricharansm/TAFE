
import os
import json
from datetime import datetime, date
from typing import Dict, List

import pandas as pd
import streamlit as st

try:
    from openai import AzureOpenAI
except Exception:
    AzureOpenAI = None


st.set_page_config(
    page_title="TAFE AI Learning Assistant Prototype",
    page_icon="🚜",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Styling
# -----------------------------
st.markdown(
    """
    <style>
    .main-header {
        padding: 1.2rem 1.4rem;
        border-radius: 18px;
        background: linear-gradient(135deg, #063b63 0%, #0b6aa2 55%, #f58220 100%);
        color: white;
        margin-bottom: 1rem;
    }
    .main-header h1 { margin-bottom: 0.2rem; }
    .metric-card {
        padding: 1rem;
        border: 1px solid #e8edf3;
        border-radius: 16px;
        background: #ffffff;
        box-shadow: 0 1px 8px rgba(0,0,0,0.04);
        min-height: 130px;
    }
    .agent-card {
        padding: 1rem;
        border-radius: 16px;
        border-left: 6px solid #0b6aa2;
        background: #f7fbff;
        margin-bottom: 0.8rem;
    }
    .nudge-card {
        padding: 0.8rem;
        border-radius: 14px;
        background: #fff8ed;
        border: 1px solid #fde4bf;
        margin-bottom: 0.6rem;
    }
    .guardrail {
        padding: 0.75rem;
        border-radius: 12px;
        background: #f6f8fa;
        border-left: 5px solid #3d6c3d;
        margin-bottom: 0.4rem;
    }
    .small-muted { color: #697386; font-size: 0.9rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Mock data
# -----------------------------
@st.cache_data
def load_data():
    learners = pd.read_csv("data/learners.csv")
    courses = pd.read_csv("data/courses.csv")
    completions = pd.read_csv("data/completions.csv")
    campaigns = pd.read_csv("data/campaigns.csv")
    return learners, courses, completions, campaigns


learners, courses, completions, campaigns = load_data()


# -----------------------------
# Optional Azure OpenAI helper
# -----------------------------
def get_azure_client():
    if AzureOpenAI is None:
        return None
    required = [
        "AZURE_OPENAI_ENDPOINT",
        "AZURE_OPENAI_API_KEY",
        "AZURE_OPENAI_DEPLOYMENT",
        "AZURE_OPENAI_API_VERSION",
    ]
    if not all(os.getenv(k) for k in required):
        return None
    return AzureOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
    )


def call_llm(system_prompt: str, user_prompt: str, fallback: str) -> str:
    """
    Uses Azure OpenAI if configured. Otherwise returns a deterministic prototype response.
    This lets the prototype run safely from GitHub without cloud dependencies.
    """
    client = get_azure_client()
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    if client and deployment:
        try:
            response = client.chat.completions.create(
                model=deployment,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.3,
                max_tokens=1000,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Azure OpenAI call failed, showing prototype response instead.\n\n{fallback}\n\nError: {e}"
    return fallback


def role_guardrail(user_role: str, content_class: str) -> bool:
    """
    Prototype guardrail. In production, this should be enforced at:
    1) Teams / app access layer
    2) Orchestrator / agent policy layer
    3) Data layer with Entra ID and row-level security
    """
    if content_class == "R&D Confidential" and user_role not in ["L&D Admin", "R&D Leader", "Leadership"]:
        return False
    return True


def learner_profile(learner_id: str) -> Dict:
    row = learners[learners["learner_id"] == learner_id].iloc[0].to_dict()
    c = completions[completions["learner_id"] == learner_id].merge(courses, on="course_id", how="left")
    row["completed_courses"] = c
    return row


def recommend_courses(profile: Dict, user_role: str) -> pd.DataFrame:
    completed = set(profile["completed_courses"]["course_id"].tolist())
    role = profile["role"]
    skills = [s.strip().lower() for s in profile["skills_to_build"].split(";")]
    available = courses[~courses["course_id"].isin(completed)].copy()
    available["score"] = 0

    available.loc[available["target_roles"].str.contains(role, case=False, na=False), "score"] += 35
    for skill in skills:
        available.loc[
            available["skills"].str.lower().str.contains(skill, na=False),
            "score",
        ] += 25

    available.loc[available["content_class"] == "Public/Internal", "score"] += 5
    available = available[available.apply(lambda r: role_guardrail(user_role, r["content_class"]), axis=1)]
    return available.sort_values(["score", "duration_minutes"], ascending=[False, True]).head(5)


# -----------------------------
# Sidebar persona
# -----------------------------
st.sidebar.image("https://dummyimage.com/600x180/063b63/ffffff&text=TAFE+AI+Learning+Prototype", use_container_width=True)
st.sidebar.title("Prototype Controls")

selected_learner_id = st.sidebar.selectbox(
    "Select learner persona",
    learners["learner_id"].tolist(),
    format_func=lambda x: f'{learners.loc[learners.learner_id == x, "name"].iloc[0]} — {learners.loc[learners.learner_id == x, "role"].iloc[0]}',
)

selected_app_role = st.sidebar.selectbox(
    "Logged-in role / access profile",
    ["Learner", "Manager", "Business Head", "L&D Admin", "R&D Leader", "Leadership"],
    index=0,
)

st.sidebar.markdown("---")
st.sidebar.caption("This is a clickable prototype. It uses mock Moodle, HR and course catalog data, with optional Azure OpenAI integration.")


profile = learner_profile(selected_learner_id)
recommended = recommend_courses(profile, selected_app_role)


# -----------------------------
# Header
# -----------------------------
st.markdown(
    f"""
    <div class="main-header">
        <h1>TAFE Learner Assistant + AI Coach</h1>
        <div>Prototype for Learning & Development: unified learner assistant, instructional designer, and learning campaigner agents.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    st.metric("Pilot Learners", f"{len(learners):,}", "Mock population")
with kpi2:
    adoption = int(completions["learner_id"].nunique() / len(learners) * 100)
    st.metric("Active Learning Adoption", f"{adoption}%", "+25% target")
with kpi3:
    st.metric("Recommended Courses", len(recommended), "Personalized")
with kpi4:
    st.metric("Guardrail Mode", selected_app_role, "Role-aware")


# -----------------------------
# Tabs
# -----------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "🏠 Command Center",
        "🎓 Learner Assistant + AI Coach",
        "🧩 Instructional Designer Agent",
        "📣 Learning Campaigner Agent",
        "🛡️ Admin & Guardrails",
    ]
)


with tab1:
    st.subheader("Unified Agent Experience")
    st.write(
        "This screen represents the proposed single employee-facing experience. "
        "The same assistant behaves differently for a learner, manager, business head, or leadership user."
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            """
            <div class="agent-card">
            <h4>🎓 Learner Assistant + AI Coach</h4>
            <p>Personalized course recommendations, learning-path Q&A, performance-gap coaching, and role-aware dashboards.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            """
            <div class="agent-card">
            <h4>🧩 Instructional Designer Agent</h4>
            <p>Turns SME inputs into learning objectives, module structures, storyboards, and authoring-ready outlines.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            """
            <div class="agent-card">
            <h4>📣 Learning Campaigner Agent</h4>
            <p>Creates learning campaigns, birthday nudges, festive nudges, reminders, and adoption-driving communications.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.subheader("Pilot Roadmap")
    roadmap = pd.DataFrame(
        [
            ["Weeks 1–2", "Foundation", "Mock/real Moodle data connection, HR profile mapping, role taxonomy, security rules"],
            ["Weeks 3–6", "Quick Win Agents", "Instructional Designer Agent and Learning Campaigner Agent MVP"],
            ["Weeks 7–10", "Learner Coach", "Personalized course recommendation, learner chat, manager views"],
            ["Weeks 11–14", "Pilot Rollout", "One business unit rollout, feedback loop, adoption and recommendation metrics"],
        ],
        columns=["Timeline", "Workstream", "Outcome"],
    )
    st.dataframe(roadmap, use_container_width=True, hide_index=True)

    st.subheader("Sample Learning Analytics")
    chart_data = completions.merge(learners[["learner_id", "function"]], on="learner_id").groupby("function").size().reset_index(name="completed_courses")
    st.bar_chart(chart_data, x="function", y="completed_courses", use_container_width=True)


with tab2:
    st.subheader("Learner Assistant + AI Learning Coach")

    left, right = st.columns([1, 2])
    with left:
        st.markdown("#### Learner Profile")
        st.write(f"**Name:** {profile['name']}")
        st.write(f"**Role:** {profile['role']}")
        st.write(f"**Function:** {profile['function']}")
        st.write(f"**Career aspiration:** {profile['career_goal']}")
        st.write(f"**Skills to build:** {profile['skills_to_build']}")
        st.write(f"**Manager:** {profile['manager']}")
        st.markdown("#### Completed Learning")
        st.dataframe(
            profile["completed_courses"][["title", "category", "completion_date", "score"]],
            use_container_width=True,
            hide_index=True,
        )

    with right:
        st.markdown("#### Personalized Recommendations")
        st.dataframe(
            recommended[["title", "category", "skills", "duration_minutes", "content_class", "score"]],
            use_container_width=True,
            hide_index=True,
        )

        st.markdown("#### Ask the Coach")
        default_question = "What should I learn next and why?"
        user_question = st.text_input("Question", value=default_question)

        if st.button("Generate coaching response", type="primary"):
            context = {
                "learner": {k: str(v) for k, v in profile.items() if k != "completed_courses"},
                "completed_courses": profile["completed_courses"][["title", "category", "score"]].to_dict(orient="records"),
                "recommended_courses": recommended[["title", "category", "skills", "duration_minutes"]].to_dict(orient="records"),
                "logged_in_role": selected_app_role,
            }

            fallback = f"""
Hi {profile['name']}, based on your role as {profile['role']} and your goal to become stronger in {profile['career_goal']}, I recommend starting with:

1. {recommended.iloc[0]['title'] if len(recommended) else 'a role-relevant learning path'}
2. {recommended.iloc[1]['title'] if len(recommended) > 1 else 'a short skill refresher'}
3. {recommended.iloc[2]['title'] if len(recommended) > 2 else 'a manager-recommended module'}

Why this path:
- It aligns to your current function: {profile['function']}.
- It builds the skills you selected: {profile['skills_to_build']}.
- It balances short courses with capability-building modules.

Suggested next step:
Complete one short course this week, then schedule a 15-minute reflection with your manager on how the learning applies to your current work.
"""
            answer = call_llm(
                "You are TAFE's AI Learning Coach. Give practical, role-aware, concise learning guidance. Do not reveal restricted content.",
                f"User question: {user_question}\nContext:\n{json.dumps(context, indent=2)}",
                fallback,
            )
            st.markdown(answer)

    st.markdown("---")
    st.markdown("#### Manager / Business Head View")
    if selected_app_role in ["Manager", "Business Head", "Leadership", "L&D Admin"]:
        team = learners[learners["manager"] == profile["manager"]]
        team_completion = completions[completions["learner_id"].isin(team["learner_id"])]
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Team Members", len(team))
        col_b.metric("Courses Completed", len(team_completion))
        col_c.metric("Avg Score", f"{team_completion['score'].mean():.1f}" if len(team_completion) else "N/A")
        st.dataframe(team[["name", "role", "function", "skills_to_build", "career_goal"]], use_container_width=True, hide_index=True)
    else:
        st.info("Manager and business-impact analytics are hidden for learner-only access.")


with tab3:
    st.subheader("Instructional Designer Agent")
    st.write(
        "This agent converts a subject-matter brief into instructional objectives, module design, storyboard structure, "
        "assessment questions, and production notes."
    )

    with st.form("id_agent_form"):
        topic = st.text_input("Training topic", "Hydraulic System Basics for Tractor Service Teams")
        audience = st.text_input("Target audience", "Dealer service technicians and junior maintenance engineers")
        duration = st.selectbox("Target duration", ["15 minutes", "30 minutes", "45 minutes", "60 minutes"], index=1)
        modality = st.selectbox("Learning format", ["E-learning module", "Instructor-led session", "Video script", "Blended learning", "XR/AR scenario"], index=0)
        source_brief = st.text_area(
            "SME input / raw brief",
            "Technicians need to understand hydraulic pump, reservoir, valves, cylinders, safety precautions, common faults, and basic troubleshooting steps.",
            height=140,
        )
        submitted = st.form_submit_button("Generate instructional design", type="primary")

    if submitted:
        fallback = f"""
### Instructional Design Draft

**Topic:** {topic}  
**Audience:** {audience}  
**Recommended modality:** {modality}  
**Target duration:** {duration}

#### 1. Learning objectives
By the end of this module, learners should be able to:
- Explain the purpose of the hydraulic pump, reservoir, valves, and cylinders.
- Identify common symptoms of hydraulic system issues.
- Apply basic safety checks before inspection or troubleshooting.
- Choose the correct first-level troubleshooting step for common faults.

#### 2. Module structure
| Section | Duration | Learning activity |
|---|---:|---|
| Context setting | 3 min | Why hydraulics matter in tractor performance |
| Concept explanation | 8 min | Visual walkthrough of key components |
| Safety checklist | 5 min | Interactive checklist |
| Common faults | 8 min | Scenario-based examples |
| Knowledge check | 6 min | 5-question quiz and feedback |

#### 3. Storyboard outline
1. Opening screen: real-world service scenario.
2. Component map: click-to-reveal pump, reservoir, valves, cylinders.
3. Safety pause: PPE, pressure release, lockout process.
4. Fault scenario: weak lift / slow response / leakage.
5. Guided troubleshooting: inspect fluid, filter, leaks, pressure.
6. Assessment: scenario-based questions.

#### 4. Assessment questions
- What is the first safety action before inspecting a hydraulic line?
- Which component converts hydraulic pressure into mechanical movement?
- A slow lifting implement may indicate which likely issue?
- Why should hydraulic pressure be released before maintenance?
- Which symptom should be escalated to a senior technician?

#### 5. Production notes
- Use consistent icons for each component.
- Include field photos or illustrations where available.
- Keep technical terms simple and define them on first use.
- Add accessibility checks for contrast, alt text, and readable font size.
"""
        output = call_llm(
            "You are an expert instructional designer for manufacturing and service training. Produce structured, authoring-ready learning design.",
            f"Topic: {topic}\nAudience: {audience}\nDuration: {duration}\nModality: {modality}\nSME Brief: {source_brief}",
            fallback,
        )
        st.markdown(output)

    st.markdown("#### Prototype Output Contract")
    st.dataframe(
        pd.DataFrame(
            [
                ["Input", "SME brief, training topic, audience, modality, duration"],
                ["Output", "Learning objectives, module flow, storyboard, assessment, production notes"],
                ["Human review", "L&D consultant validates accuracy and tone before production"],
                ["System of record", "SharePoint / Moodle authoring folder"],
            ],
            columns=["Area", "Description"],
        ),
        hide_index=True,
        use_container_width=True,
    )


with tab4:
    st.subheader("Learning Campaigner Agent")
    st.write(
        "This agent plans learning campaigns and creates personalized nudges using HR events, Moodle history, role context, "
        "and campaign calendars."
    )

    campaign_col, learner_col = st.columns([1, 1])
    with campaign_col:
        campaign_name = st.selectbox("Campaign", campaigns["campaign_name"].tolist())
        campaign = campaigns[campaigns["campaign_name"] == campaign_name].iloc[0]
        st.write(f"**Theme:** {campaign['theme']}")
        st.write(f"**Target audience:** {campaign['target_audience']}")
        st.write(f"**Recommended channel:** {campaign['channel']}")

    with learner_col:
        nudge_style = st.selectbox("Nudge style", ["Warm and encouraging", "Manager-like", "Festive", "Crisp and action-oriented"])
        nudge_goal = st.text_input("Nudge goal", "Encourage learner to start one short course this week")

    if st.button("Generate campaign nudges", type="primary"):
        candidate_learners = learners.sample(min(4, len(learners)), random_state=7)
        for _, learner in candidate_learners.iterrows():
            recs = recommend_courses(learner_profile(learner["learner_id"]), selected_app_role)
            course_title = recs.iloc[0]["title"] if len(recs) else "a recommended learning module"
            fallback = f"""
<div class="nudge-card">
<b>To: {learner['name']}</b><br/>
Hi {learner['name']}, here is a quick learning suggestion for you: <b>{course_title}</b>.<br/>
It aligns with your role as {learner['role']} and supports your growth goal: {learner['career_goal']}. 
Can you spend 20 minutes this week and get started?
</div>
"""
            prompt = f"""
Campaign: {campaign_name}
Campaign theme: {campaign['theme']}
Learner: {learner.to_dict()}
Recommended course: {course_title}
Style: {nudge_style}
Goal: {nudge_goal}
"""
            generated = call_llm(
                "You are a learning campaign agent. Write one short, personalized, culturally appropriate learning nudge. Keep it under 80 words.",
                prompt,
                fallback,
            )
            st.markdown(generated, unsafe_allow_html=True)

    st.markdown("#### Campaign Calendar")
    st.dataframe(campaigns, use_container_width=True, hide_index=True)


with tab5:
    st.subheader("Admin & Guardrails")
    st.write(
        "This tab demonstrates how the prototype enforces role-aware access to learning content. "
        "Production implementation should use Entra ID groups, orchestrator policies, and row-level security."
    )

    st.markdown("#### Three-Layer Guardrail Model")
    st.markdown(
        """
        <div class="guardrail"><b>1. App / Teams access:</b> Only authenticated TAFE users can access the assistant.</div>
        <div class="guardrail"><b>2. Orchestrator policy:</b> The agent checks user role, function, manager hierarchy, and content class before answering.</div>
        <div class="guardrail"><b>3. Data security:</b> Moodle, HR, SharePoint, and analytics data are filtered using Entra ID and row-level permissions.</div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("#### Course Access Simulation")
    access_rows = []
    for _, row in courses.iterrows():
        access_rows.append(
            {
                "course": row["title"],
                "content_class": row["content_class"],
                "logged_in_role": selected_app_role,
                "visible": "Yes" if role_guardrail(selected_app_role, row["content_class"]) else "No — restricted",
            }
        )
    st.dataframe(pd.DataFrame(access_rows), use_container_width=True, hide_index=True)

    st.markdown("#### Agent Configuration")
    config = {
        "learner_assistant": {
            "temperature": 0.3,
            "tools": ["moodle_search", "course_recommendation", "learning_history", "manager_dashboard"],
            "guardrails": ["role_filtering", "content_class_filtering", "no_rnd_disclosure"],
        },
        "instructional_designer": {
            "temperature": 0.4,
            "tools": ["storyboard_generator", "objective_builder", "assessment_builder"],
            "guardrails": ["human_review_required", "source_traceability"],
        },
        "learning_campaigner": {
            "temperature": 0.6,
            "tools": ["campaign_calendar", "hr_events", "moodle_history", "teams_nudge"],
            "guardrails": ["no_sensitive_personalization", "opt_out_respected"],
        },
    }
    st.json(config)

    st.markdown("#### Environment Status")
    if get_azure_client():
        st.success("Azure OpenAI configuration detected.")
    else:
        st.warning("Azure OpenAI is not configured. The app is running in deterministic prototype mode.")
