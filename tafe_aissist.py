import streamlit as st
import random
from datetime import datetime, timedelta
import time

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="TAFE AIssist",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Brand palette (TAFE: red #CC0000, green #2D7A27, dark navy #1A2B4A) ──────
TAFE_RED   = "#CC0000"
TAFE_GREEN = "#2D7A27"
TAFE_NAVY  = "#1A2B4A"
TAFE_CREAM = "#F7F4EF"
TAFE_GREY  = "#F0F0F0"

st.markdown(f"""
<style>
  /* ── Global resets ── */
  [data-testid="stAppViewContainer"] {{ background: {TAFE_CREAM}; }}
  [data-testid="stSidebar"]          {{ background: {TAFE_NAVY}; }}
  [data-testid="stSidebar"] * {{ color: #E8E8E8 !important; }}
  [data-testid="stSidebar"] .stSelectbox label {{ color: #aaa !important; font-size:0.75rem; }}

  /* ── Top bar logo strip ── */
  .top-bar {{
    background: {TAFE_NAVY};
    color: white;
    padding: 12px 24px;
    display: flex;
    align-items: center;
    gap: 16px;
    border-radius: 10px;
    margin-bottom: 20px;
  }}
  .top-bar .brand {{ font-size: 1.6rem; font-weight: 800; color: {TAFE_RED}; letter-spacing:1px; }}
  .top-bar .sub   {{ font-size: 0.85rem; color: #ccc; }}
  .top-bar .badge {{
    margin-left: auto;
    background: {TAFE_GREEN};
    color: white;
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.78rem;
    font-weight: 600;
  }}

  /* ── Agent cards ── */
  .agent-card {{
    background: white;
    border-radius: 12px;
    padding: 20px 24px;
    border-left: 4px solid {TAFE_RED};
    margin-bottom: 16px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  }}
  .agent-card h3 {{ margin:0 0 4px 0; color: {TAFE_NAVY}; font-size: 1rem; }}
  .agent-card p  {{ margin:0; color: #666; font-size: 0.84rem; }}

  /* ── Chat bubbles ── */
  .chat-user {{
    background: {TAFE_NAVY};
    color: white;
    border-radius: 18px 18px 4px 18px;
    padding: 12px 18px;
    margin: 8px 0 8px 20%;
    font-size: 0.9rem;
    line-height: 1.5;
  }}
  .chat-ai {{
    background: white;
    border: 1px solid #e0e0e0;
    border-radius: 18px 18px 18px 4px;
    padding: 14px 18px;
    margin: 8px 20% 8px 0;
    font-size: 0.9rem;
    line-height: 1.6;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
  }}
  .chat-ai .ai-label {{
    font-size: 0.72rem;
    color: {TAFE_RED};
    font-weight: 700;
    letter-spacing: 0.5px;
    margin-bottom: 6px;
  }}

  /* ── Metric tiles ── */
  .metric-tile {{
    background: white;
    border-radius: 10px;
    padding: 16px 20px;
    text-align: center;
    box-shadow: 0 1px 6px rgba(0,0,0,0.07);
  }}
  .metric-tile .val {{ font-size: 2rem; font-weight: 800; color: {TAFE_NAVY}; }}
  .metric-tile .lbl {{ font-size: 0.78rem; color: #888; margin-top:2px; }}
  .metric-tile .delta {{ font-size: 0.78rem; color: {TAFE_GREEN}; font-weight: 600; }}

  /* ── Section headers ── */
  .sec-header {{
    font-size: 1.15rem;
    font-weight: 700;
    color: {TAFE_NAVY};
    border-bottom: 2px solid {TAFE_RED};
    padding-bottom: 6px;
    margin-bottom: 16px;
  }}

  /* ── Tags / pills ── */
  .pill {{
    display: inline-block;
    background: {TAFE_GREY};
    color: {TAFE_NAVY};
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 0.76rem;
    font-weight: 600;
    margin: 2px;
  }}
  .pill-green {{ background: #e6f4e5; color: {TAFE_GREEN}; }}
  .pill-red   {{ background: #fdeaea; color: {TAFE_RED};   }}

  /* ── Storyboard block ── */
  .storyboard {{
    background: white;
    border-radius: 10px;
    padding: 16px 20px;
    border: 1px solid #e0e0e0;
    margin-bottom: 12px;
  }}
  .storyboard h4 {{ margin: 0 0 6px 0; color: {TAFE_NAVY}; font-size: 0.95rem; }}
  .storyboard p  {{ margin: 0; color: #555; font-size: 0.85rem; line-height:1.5; }}

  /* ── Campaign card ── */
  .campaign-card {{
    background: white;
    border-radius: 12px;
    padding: 18px 22px;
    border-top: 4px solid {TAFE_GREEN};
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    margin-bottom: 14px;
  }}
  .campaign-card h4 {{ margin: 0 0 4px 0; color: {TAFE_NAVY}; }}
  .campaign-card .nudge-preview {{
    background: {TAFE_CREAM};
    border-radius: 8px;
    padding: 12px;
    margin-top: 10px;
    font-size: 0.85rem;
    color: #444;
    font-style: italic;
    line-height: 1.5;
  }}

  /* Hide streamlit branding */
  #MainMenu, footer, header {{ visibility: hidden; }}
  .stDeployButton {{ display:none; }}

  div[data-testid="stHorizontalBlock"] > div {{ padding: 0 6px; }}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# Mock data
# ══════════════════════════════════════════════════════════════════════════════

LEARNER_PROFILES = {
    "Arjun Mehta (Engineer — Powertrain)": {
        "role": "Engineer", "dept": "Powertrain", "level": "Mid",
        "completed": 14, "in_progress": 3, "overdue": 1,
        "completion_rate": 72, "hours_ytd": 38,
        "skills": ["Hydraulics", "Engine Calibration", "Quality Standards"],
        "gaps": ["Safety Compliance (overdue)", "Advanced CAD"],
        "recommended": [
            ("ISO 9001 Quality Management for Engineers", "Compliance", "2h 30m"),
            ("Advanced CAD Design Principles", "Technical", "4h"),
            ("Lean Manufacturing Fundamentals", "Operations", "3h"),
        ],
        "career_goal": "Senior Design Engineer",
    },
    "Priya Venkat (Manager — Sales)": {
        "role": "Manager", "dept": "Sales", "level": "Senior",
        "completed": 22, "in_progress": 2, "overdue": 0,
        "completion_rate": 91, "hours_ytd": 61,
        "skills": ["Product Knowledge", "CRM", "Dealer Relations"],
        "gaps": ["AI for Sales Leaders", "Financial Acumen"],
        "recommended": [
            ("AI Tools for Sales Leaders", "Leadership", "2h"),
            ("Financial Acumen for Non-Finance Managers", "Business", "3h 30m"),
            ("Advanced Negotiation Techniques", "Sales", "2h 30m"),
        ],
        "career_goal": "Regional Sales Director",
        "team_size": 12,
        "team_completion": 68,
    },
    "Dr. Ramesh Iyer (President — R&D)": {
        "role": "Leadership", "dept": "R&D", "level": "C-Suite",
        "completed": 8, "in_progress": 1, "overdue": 0,
        "completion_rate": 88, "hours_ytd": 18,
        "skills": ["Strategic Leadership", "Innovation Management"],
        "gaps": ["GenAI for R&D Leaders"],
        "recommended": [
            ("GenAI for R&D and Innovation Leaders", "Leadership", "1h 30m"),
            ("IP Management in Manufacturing", "Legal", "2h"),
        ],
        "career_goal": "—",
        "team_size": 240,
        "team_completion": 54,
        "access_level": "r&d_confidential",
    },
}

CAMPAIGN_EVENTS = [
    {
        "name": "🎂 Birthday Learning Nudge",
        "type": "Birthday",
        "trigger": "Daily at 8:00 AM",
        "reach": "~12 employees/day",
        "channel": "Microsoft Teams",
        "nudge": "Hi Suresh! 🎂 Happy Birthday from TAFE L&D! It's a great day to invest 20 minutes in yourself — we've picked a short module on {topic} that fits your current role. Start it now and celebrate growth! 🌾",
        "status": "Active",
        "sent_30d": 342,
        "open_rate": 67,
        "start_rate": 41,
    },
    {
        "name": "📚 World Book Day",
        "type": "Cultural",
        "trigger": "April 23 (annual)",
        "reach": "All 4,200 employees",
        "channel": "Teams + Email",
        "nudge": "Hi {name}! Today is World Book Day 📚 — and learning is at the heart of TAFE's culture. We've curated a 30-minute reading challenge from our knowledge library. Join 847 colleagues who've already started today!",
        "status": "Completed",
        "sent_30d": 4200,
        "open_rate": 72,
        "start_rate": 38,
    },
    {
        "name": "🚜 Farmer's Day Learning Sprint",
        "type": "Brand",
        "trigger": "December 23 (annual)",
        "reach": "All employees",
        "channel": "Teams + Moodle Banner",
        "nudge": "Happy Farmer's Day! 🌾 As TAFE employees, we celebrate the farmers we serve every day. This week's sprint: complete one module from our Product Knowledge series and earn a special Farmer's Day badge.",
        "status": "Draft",
        "sent_30d": 0,
        "open_rate": 0,
        "start_rate": 0,
    },
    {
        "name": "🪔 Diwali Learning Celebration",
        "type": "Cultural",
        "trigger": "Diwali (Nov)",
        "reach": "India offices",
        "channel": "Teams",
        "nudge": "Diwali Greetings! 🪔 May this festival of lights also light up your learning journey. We've lined up a short, festive 15-minute module — a gift from L&D to you. Wishing you and your family a joyful Diwali!",
        "status": "Active",
        "sent_30d": 1840,
        "open_rate": 81,
        "start_rate": 55,
    },
]

STORYBOARD_MODULES = {
    "New Product Introduction — TAFE DIVA Pro Tractor": {
        "objectives": [
            "Describe the key differentiators of TAFE DIVA Pro vs. previous generation",
            "Explain the 4WD transmission mechanism and maintenance schedule",
            "Identify common dealer FAQs and respond with confidence",
        ],
        "audience": "Dealer network, Sales Engineers",
        "duration": "45 minutes",
        "format": "SCORM e-learning + embedded video",
        "modules": [
            {
                "seq": "01",
                "title": "Welcome & Product Overview",
                "type": "Intro Screen",
                "narration": "Open with the TAFE DIVA Pro hero shot. Narrator: 'Meet the next evolution of precision farming...' Transition to feature comparison table vs. DIVA Standard.",
                "duration": "3 min",
                "assets": "Hero video (60s), feature comparison graphic",
            },
            {
                "seq": "02",
                "title": "Engine & Powertrain Deep Dive",
                "type": "Explainer + Diagram",
                "narration": "Animated 3D cutaway of the 50HP engine. Callout labels highlight: turbocharged intake, dual-stage filtration, Agri-ECU. Knowledge check: drag-and-drop component identification.",
                "duration": "10 min",
                "assets": "3D engine model (Unity), labeled diagram PNG",
            },
            {
                "seq": "03",
                "title": "4WD Transmission & Field Applications",
                "type": "Scenario-based",
                "narration": "Branching scenario: farmer selects terrain type (paddy, upland, orchard) — learner must choose the correct gear range and 4WD mode. Wrong answers show consequences with corrective feedback.",
                "duration": "12 min",
                "assets": "Branching scenario (Articulate), terrain photos",
            },
            {
                "seq": "04",
                "title": "Dealer Q&A Simulator",
                "type": "Conversational AI Practice",
                "narration": "AI-powered role-play: simulated customer asks pricing, comparison with John Deere, warranty. Learner types responses; AI scores on accuracy and confidence language.",
                "duration": "12 min",
                "assets": "AIssist Q&A module integration",
            },
            {
                "seq": "05",
                "title": "Assessment & Certification",
                "type": "Quiz + Badge",
                "narration": "20-question adaptive quiz. Pass mark 80%. On pass: 'TAFE DIVA Pro Certified' digital badge issued to Moodle profile. On fail: targeted remediation loop to weak modules.",
                "duration": "8 min",
                "assets": "Quiz bank (40 Qs), badge graphic",
            },
        ],
        "wcag_flags": [],
        "id_notes": "Ensure all diagrams have ALT text. Avoid red/green only color coding for color-blind accessibility. Narration script to be reviewed by Product team before voice recording.",
    },
    "Safety Compliance — Working at Height (Annual Mandatory)": {
        "objectives": [
            "Identify hazardous situations requiring fall protection equipment",
            "Correctly apply the hierarchy of controls for working at height",
            "Complete the annual compliance acknowledgment",
        ],
        "audience": "All plant and shop-floor employees (mandatory)",
        "duration": "30 minutes",
        "format": "SCORM e-learning",
        "modules": [
            {
                "seq": "01",
                "title": "Why Safety Matters at TAFE",
                "type": "Video + Acknowledgment",
                "narration": "CEO message video (2 min). Key stats: 0 LTI target. Emotional hook: real (anonymised) near-miss story. Learner clicks 'I commit to safe practices' to proceed.",
                "duration": "4 min",
                "assets": "CEO video, acknowledgment widget",
            },
            {
                "seq": "02",
                "title": "Hazard Identification — Spot the Risk",
                "type": "Hotspot Interaction",
                "narration": "360° photo of a workshop scene. Learner clicks on hazards they can identify. 8 hotspots: 3 correct (ladder without foot, unsecured tool, no harness). Feedback per click.",
                "duration": "8 min",
                "assets": "360° scene photo, hotspot config",
            },
            {
                "seq": "03",
                "title": "Hierarchy of Controls",
                "type": "Drag-and-Drop",
                "narration": "Pyramid diagram. Learner drags 6 control types to the correct level (Elimination → Substitution → Engineering → Administrative → PPE). Animated reveal on completion.",
                "duration": "6 min",
                "assets": "Hierarchy diagram, drag-drop interaction",
            },
            {
                "seq": "04",
                "title": "Compliance Assessment",
                "type": "Graded Quiz",
                "narration": "15 questions. 100% pass required (mandatory compliance). Unlimited attempts. Completion auto-records in Moodle for HR audit trail.",
                "duration": "12 min",
                "assets": "Question bank (30 Qs, randomised draw)",
            },
        ],
        "wcag_flags": ["Ensure all videos have captions", "Hotspot targets must be keyboard-navigable"],
        "id_notes": "This is a mandatory course — zero tolerance for gamification elements that trivialise safety. Tone: serious, respectful. Legal review of compliance language required before publish.",
    },
}

QA_CHECKLIST_ITEMS = [
    ("Visual Consistency", "Fonts match TAFE brand guide (Calibri body, TAFE Red headers)", True),
    ("Visual Consistency", "Colour palette compliant — no unapproved hex values", True),
    ("Visual Consistency", "Logo usage correct — not distorted, on approved backgrounds", True),
    ("Instructional Integrity", "Learning objectives stated on slide 1", True),
    ("Instructional Integrity", "Each objective addressed by at least one activity", True),
    ("Instructional Integrity", "Knowledge checks present every 10 minutes", False),
    ("Accessibility", "All images have descriptive ALT text", False),
    ("Accessibility", "Colour contrast ratio ≥ 4.5:1 for body text", True),
    ("Accessibility", "Videos include closed captions", False),
    ("Technical", "SCORM package tested in Moodle staging", True),
    ("Technical", "Module completes on pass of final assessment", True),
    ("Technical", "Progress saved on mid-module exit", True),
]

# ══════════════════════════════════════════════════════════════════════════════
# Sidebar navigation
# ══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("""
    <div style='padding:10px 0 20px 0; border-bottom: 1px solid #334; margin-bottom:20px;'>
      <div style='font-size:1.4rem; font-weight:800; color:#CC0000; letter-spacing:1px;'>TAFE</div>
      <div style='font-size:0.78rem; color:#aaa; margin-top:2px;'>AI(ssist) Platform · L&D Edition</div>
    </div>
    """, unsafe_allow_html=True)

    agent = st.radio(
        "Choose Agent",
        [
            "🎓 Learner Assistant + AI Coach",
            "✏️ Instructional Designer Agent",
            "📣 Learning Campaigner Agent",
        ],
        label_visibility="collapsed",
    )

    st.markdown("<div style='margin-top:30px; font-size:0.72rem; color:#556; text-transform:uppercase; letter-spacing:1px;'>Platform</div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:0.82rem; color:#99a; line-height:1.8;'>
    ⚙️ Azure AI Foundry<br>
    🔗 Moodle LMS (on-prem)<br>
    👤 Entra ID (identity)<br>
    💬 Microsoft Teams surface<br>
    📊 Power BI analytics
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:30px; font-size:0.72rem; color:#556; text-transform:uppercase; letter-spacing:1px;'>Status</div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:0.8rem; line-height:1.9;'>
    <span style='color:#4CAF50;'>●</span> Moodle connector live<br>
    <span style='color:#4CAF50;'>●</span> HR system synced<br>
    <span style='color:#4CAF50;'>●</span> R&D guardrails active<br>
    <span style='color:#FFA500;'>●</span> Analytics (Phase 2)
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""<div style='margin-top:40px; font-size:0.72rem; color:#445; border-top:1px solid #334; padding-top:12px;'>
    Powered by Saxon · Microsoft Azure<br>Built on AIssist V2 platform<br><span style='color:{TAFE_RED};'>Prototype · May 2026</span>
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# Top bar
# ══════════════════════════════════════════════════════════════════════════════

agent_titles = {
    "🎓 Learner Assistant + AI Coach": ("Learner Assistant + AI Coach", "UC-4 · Strategic POC · Phase 1 Flagship"),
    "✏️ Instructional Designer Agent": ("Instructional Designer Agent", "UC-1 · Quick Win · Phase 1"),
    "📣 Learning Campaigner Agent": ("Learning Campaigner Agent", "UC-3 · Quick Win · Phase 1"),
}
title, subtitle = agent_titles[agent]

st.markdown(f"""
<div class="top-bar">
  <div>
    <div class="brand">TAFE · AI(ssist)</div>
    <div class="sub">{subtitle}</div>
  </div>
  <div style='font-size:1.1rem; font-weight:700; color:white; margin-left:20px;'>{title}</div>
  <div class="badge">🌾 L&D Platform</div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# AGENT 1 — Learner Assistant + AI Coach
# ══════════════════════════════════════════════════════════════════════════════

if agent == "🎓 Learner Assistant + AI Coach":

    # Role selector
    col_role, col_learner, _ = st.columns([1.4, 2, 2])
    with col_role:
        role_view = st.selectbox("View as", ["Learner", "Manager", "Business Head / Leadership"])
    with col_learner:
        if role_view == "Learner":
            selected_user = st.selectbox("Learner profile", [k for k in LEARNER_PROFILES if "Engineer" in k or "Venkat" in k])
        elif role_view == "Manager":
            selected_user = "Priya Venkat (Manager — Sales)"
        else:
            selected_user = "Dr. Ramesh Iyer (President — R&D)"

    profile = LEARNER_PROFILES[selected_user]
    st.markdown("---")

    # ── Learner view ──────────────────────────────────────────────────────────
    if role_view == "Learner":
        left, right = st.columns([1.1, 2])

        with left:
            st.markdown('<div class="sec-header">My Learning Profile</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="agent-card">
              <h3>{selected_user.split('(')[0].strip()}</h3>
              <p>{profile['role']} · {profile['dept']} · {profile['level']}</p>
              <p style='margin-top:8px;'>🎯 Career goal: <b>{profile['career_goal']}</b></p>
            </div>
            """, unsafe_allow_html=True)

            mc1, mc2, mc3 = st.columns(3)
            with mc1:
                st.markdown(f'<div class="metric-tile"><div class="val">{profile["completed"]}</div><div class="lbl">Completed</div></div>', unsafe_allow_html=True)
            with mc2:
                st.markdown(f'<div class="metric-tile"><div class="val">{profile["in_progress"]}</div><div class="lbl">In Progress</div></div>', unsafe_allow_html=True)
            with mc3:
                color = "red" if profile["overdue"] > 0 else TAFE_GREEN
                st.markdown(f'<div class="metric-tile"><div class="val" style="color:{color}">{profile["overdue"]}</div><div class="lbl">Overdue</div></div>', unsafe_allow_html=True)

            st.markdown(f"""
            <div style='background:white; border-radius:10px; padding:14px 18px; margin-top:14px; box-shadow:0 1px 4px rgba(0,0,0,0.06);'>
              <div style='font-size:0.8rem; color:#888; margin-bottom:6px;'>Completion Rate</div>
              <div style='background:#eee; border-radius:20px; height:10px;'>
                <div style='background:{TAFE_GREEN}; width:{profile["completion_rate"]}%; height:10px; border-radius:20px;'></div>
              </div>
              <div style='font-size:0.85rem; font-weight:700; color:{TAFE_NAVY}; margin-top:6px;'>{profile["completion_rate"]}% · {profile["hours_ytd"]}h YTD</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div style="font-size:0.82rem; color:#888; margin-bottom:6px;">Current Skills</div>', unsafe_allow_html=True)
            pills = " ".join([f'<span class="pill pill-green">{s}</span>' for s in profile["skills"]])
            st.markdown(pills, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div style="font-size:0.82rem; color:#888; margin-bottom:6px;">Skill Gaps</div>', unsafe_allow_html=True)
            pills_gap = " ".join([f'<span class="pill pill-red">{s}</span>' for s in profile["gaps"]])
            st.markdown(pills_gap, unsafe_allow_html=True)

        with right:
            st.markdown('<div class="sec-header">AI Learning Coach</div>', unsafe_allow_html=True)

            # Chat history
            if "lc_chat" not in st.session_state:
                name_short = selected_user.split(" ")[0]
                st.session_state.lc_chat = [
                    ("ai", f"Hi {name_short}! 👋 I'm your TAFE Learning Coach. I can see you have **{profile['overdue']} overdue module** and your completion rate is at **{profile['completion_rate']}%** this quarter. Here's what I'd suggest tackling first — want me to walk you through your top recommendations?"),
                ]

            for role_msg, msg in st.session_state.lc_chat:
                if role_msg == "user":
                    st.markdown(f'<div class="chat-user">{msg}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="chat-ai"><div class="ai-label">🤖 TAFE AI Coach</div>{msg}</div>', unsafe_allow_html=True)

            # Quick prompts
            st.markdown("<br>", unsafe_allow_html=True)
            qp_cols = st.columns(3)
            quick_prompts = [
                "Show my recommendations",
                "What's overdue?",
                "Help me build a learning plan",
            ]
            for i, qp in enumerate(quick_prompts):
                if qp_cols[i].button(qp, use_container_width=True):
                    st.session_state.lc_chat.append(("user", qp))
                    name_short = selected_user.split(" ")[0]
                    if "recommend" in qp.lower():
                        recs = profile["recommended"]
                        rec_html = "".join([f"<br>**{i+1}. {r[0]}** <span style='color:#888; font-size:0.82rem;'>({r[1]} · {r[2]})</span>" for i, r in enumerate(recs)])
                        reply = f"Here are your top 3 recommended courses, personalised to your role and skill gaps:{rec_html}<br><br>Would you like to start the first one now?"
                    elif "overdue" in qp.lower():
                        reply = f"You have **1 overdue module**: *{profile['gaps'][0]}*. It was due 12 days ago. I'd recommend completing it this week — I can send you a reminder at a time that suits you. Want me to block 2 hours in your Teams calendar?"
                    else:
                        reply = f"Great idea, {name_short}! Based on your goal to become a **{profile['career_goal']}**, here's a suggested 90-day learning sprint:\n\n**Month 1:** Clear your overdue module + complete 2 foundational courses.\n**Month 2:** Tackle your top skill gap — {profile['gaps'][-1]}.\n**Month 3:** One stretch course aligned to your next role.\n\nShall I add these to your Moodle learning path?"
                    st.session_state.lc_chat.append(("ai", reply))
                    st.rerun()

            user_input = st.text_input("Ask your AI Coach anything…", placeholder="e.g. Which course should I do next?", key="lc_input")
            if st.button("Send →", key="lc_send") and user_input:
                st.session_state.lc_chat.append(("user", user_input))
                name_short = selected_user.split(" ")[0]
                reply = f"Great question, {name_short}! Based on your profile and current learning history, I'd recommend starting with **{profile['recommended'][0][0]}** — it directly addresses your skill gap in **{profile['gaps'][-1]}** and is aligned with your goal of becoming a {profile['career_goal']}. It's only {profile['recommended'][0][2]} long. Want me to enroll you?"
                st.session_state.lc_chat.append(("ai", reply))
                st.rerun()

            st.markdown('<div style="font-size:0.78rem; color:#aaa; margin-top:8px;">AI Coach is grounded in your Moodle records · All recommendations cite source data · Human review on all enrollments</div>', unsafe_allow_html=True)

    # ── Manager view ──────────────────────────────────────────────────────────
    elif role_view == "Manager":
        st.markdown('<div class="sec-header">Team Learning Dashboard — Priya Venkat · Sales (12 Reports)</div>', unsafe_allow_html=True)

        m1, m2, m3, m4 = st.columns(4)
        metrics = [
            ("68%", "Team Completion Rate", "▲ 9% vs. last quarter"),
            ("8", "Overdue (team)", "2 critical — action needed"),
            ("3", "On Track for Goals", "of 12 team members"),
            ("47h", "Avg Hours YTD", "▲ 6h vs. last quarter"),
        ]
        for col, (val, lbl, delta) in zip([m1, m2, m3, m4], metrics):
            col.markdown(f'<div class="metric-tile"><div class="val">{val}</div><div class="lbl">{lbl}</div><div class="delta">{delta}</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        left, right = st.columns(2)

        with left:
            st.markdown('<div class="sec-header">Team Members — Completion Status</div>', unsafe_allow_html=True)
            team = [
                ("Suresh Kumar", "Sales Exec", 92, "On Track", TAFE_GREEN),
                ("Meena Raj", "Sales Exec", 78, "On Track", TAFE_GREEN),
                ("Anand P.", "Area Manager", 65, "At Risk", "#FFA500"),
                ("Divya S.", "Sales Exec", 55, "At Risk", "#FFA500"),
                ("Karthik M.", "Key Accounts", 30, "Overdue", TAFE_RED),
                ("Raj Patel", "Sales Exec", 82, "On Track", TAFE_GREEN),
            ]
            for name, role_t, pct, status, color in team:
                st.markdown(f"""
                <div style='background:white; border-radius:8px; padding:10px 14px; margin-bottom:8px; display:flex; align-items:center; gap:12px; box-shadow:0 1px 3px rgba(0,0,0,0.05);'>
                  <div style='flex:1;'>
                    <div style='font-weight:600; font-size:0.88rem; color:{TAFE_NAVY};'>{name} <span style='font-weight:400; color:#888;'>· {role_t}</span></div>
                    <div style='background:#eee; border-radius:20px; height:6px; margin-top:5px;'>
                      <div style='background:{color}; width:{pct}%; height:6px; border-radius:20px;'></div>
                    </div>
                  </div>
                  <div style='font-size:0.82rem; font-weight:700; color:{color}; min-width:70px; text-align:right;'>{pct}% · {status}</div>
                </div>
                """, unsafe_allow_html=True)

        with right:
            st.markdown('<div class="sec-header">AI Manager Coach</div>', unsafe_allow_html=True)
            if "mc_chat" not in st.session_state:
                st.session_state.mc_chat = [
                    ("ai", "Hi Priya! Your team's overall completion is **68%** — up 9 points from last quarter. 🎉 However, **Karthik M.** is critically overdue on 3 mandatory courses. I can draft a personalised nudge to him, or escalate to HR if needed. What would you like to do?"),
                ]
            for role_msg, msg in st.session_state.mc_chat:
                if role_msg == "user":
                    st.markdown(f'<div class="chat-user">{msg}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="chat-ai"><div class="ai-label">🤖 TAFE Manager Coach</div>{msg}</div>', unsafe_allow_html=True)

            if st.button("Send nudge to Karthik", key="nudge_karthik"):
                st.session_state.mc_chat.append(("user", "Send nudge to Karthik"))
                st.session_state.mc_chat.append(("ai", "Done! ✅ A personalised Teams message has been queued for Karthik M.: *'Hi Karthik — I noticed you have 3 overdue modules including Safety Compliance (mandatory). I've cleared a 2-hour slot in your calendar this Thursday. Let's get these done — I'm here if you need support. — Priya'*. He'll receive it at 9 AM tomorrow. I'll notify you when he completes."))
                st.rerun()

            mi = st.text_input("Ask about your team…", placeholder="Who needs my attention most?", key="mc_input")
            if st.button("Ask →", key="mc_send") and mi:
                st.session_state.mc_chat.append(("user", mi))
                st.session_state.mc_chat.append(("ai", "Based on completion rates and overdue status, **Karthik M.** and **Divya S.** need the most immediate attention. Karthik has 3 overdue mandatory modules; Divya's at-risk on 2. I'd suggest a 1:1 check-in with both this week alongside the automated nudge I've already queued."))
                st.rerun()

    # ── Leadership view ───────────────────────────────────────────────────────
    else:
        st.markdown('<div class="sec-header">Business Impact Dashboard — R&D Function (240 Employees)</div>', unsafe_allow_html=True)
        st.markdown('<span class="pill pill-red">🔒 R&D Confidential Access</span>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        m1, m2, m3, m4 = st.columns(4)
        for col, (val, lbl, delta) in zip([m1, m2, m3, m4], [
            ("54%", "Org Completion", "▲ 11% vs. H1"),
            ("6,840h", "Learning Hours YTD", "org-wide"),
            ("3", "Critical Gaps", "safety compliance"),
            ("92%", "NPI Readiness", "DIVA Pro launch"),
        ]):
            col.markdown(f'<div class="metric-tile"><div class="val">{val}</div><div class="lbl">{lbl}</div><div class="delta">{delta}</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        left2, right2 = st.columns([1.5, 1])
        with left2:
            st.markdown('<div class="sec-header">Conversational Analytics</div>', unsafe_allow_html=True)
            if "exec_chat" not in st.session_state:
                st.session_state.exec_chat = [
                    ("ai", "Good morning, Dr. Iyer! Your R&D function's learning adoption is at **54%** — 11 points up from H1. **NPI readiness for DIVA Pro stands at 92%**, with 8 engineers yet to complete the product certification. Would you like a breakdown by sub-team, or an action plan for the remaining 8?"),
                ]
            for role_msg, msg in st.session_state.exec_chat:
                if role_msg == "user":
                    st.markdown(f'<div class="chat-user">{msg}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="chat-ai"><div class="ai-label">🤖 TAFE Executive Analytics</div>{msg}</div>', unsafe_allow_html=True)

            eq_cols = st.columns(3)
            exec_qs = ["Who are my best learners?", "Which teams have gaps?", "NPI readiness report"]
            for i, eq in enumerate(exec_qs):
                if eq_cols[i].button(eq, key=f"eq_{i}"):
                    st.session_state.exec_chat.append(("user", eq))
                    if "best" in eq.lower():
                        reply = "Your top 5 learners this quarter by hours and completion rate: **Arun T.** (98%, 42h), **Sneha G.** (96%, 38h), **Vikram N.** (94%, 35h), **Preethi A.** (92%, 33h), **Mohan R.** (90%, 31h). All 5 are in the Advanced Engineering sub-team. Their average completion is 12 points above org average."
                    elif "gap" in eq.lower():
                        reply = "3 sub-teams show significant learning gaps: **Field Testing** (38% completion — safety modules critical), **Electronics & Embedded** (44% completion — new product cert at risk), **Prototyping** (52% — manageable). I'd recommend a targeted sprint campaign for Field Testing this month."
                    else:
                        reply = "**DIVA Pro NPI Readiness: 92%** (220 of 240 engineers certified). 8 remaining engineers are in the Field Testing team — all have been nudged. At current pace, 100% certification expected by June 28. Risk: LOW. No launch readiness concerns."
                    st.session_state.exec_chat.append(("ai", reply))
                    st.rerun()

            ex_input = st.text_input("Ask the analytics engine…", placeholder="How much capability learning has R&D done this quarter?", key="exec_input")
            if st.button("Query →", key="exec_send") and ex_input:
                st.session_state.exec_chat.append(("user", ex_input))
                st.session_state.exec_chat.append(("ai", f"Analysing R&D learning data… Your function completed **{random.randint(1200,1800)} capability learning hours** this quarter — a **{random.randint(10,20)}% increase** vs. Q4 FY25. Top capability areas: Product Engineering (840h), Safety (320h), Leadership (210h). Trending up: AI & Digital Tools (+68% YoY)."))
                st.rerun()

        with right2:
            st.markdown('<div class="sec-header">Function Heatmap</div>', unsafe_allow_html=True)
            teams = [("Advanced Engineering", 88), ("Electronics & Embedded", 44), ("Field Testing", 38), ("Prototyping", 52), ("R&D Management", 91), ("Quality Assurance", 77)]
            for team_n, pct in teams:
                color = TAFE_GREEN if pct >= 75 else ("#FFA500" if pct >= 50 else TAFE_RED)
                st.markdown(f"""
                <div style='background:white; border-radius:8px; padding:9px 14px; margin-bottom:7px; box-shadow:0 1px 3px rgba(0,0,0,0.05);'>
                  <div style='display:flex; justify-content:space-between; font-size:0.85rem; margin-bottom:4px;'>
                    <span style='color:{TAFE_NAVY}; font-weight:600;'>{team_n}</span>
                    <span style='color:{color}; font-weight:700;'>{pct}%</span>
                  </div>
                  <div style='background:#eee; border-radius:20px; height:6px;'>
                    <div style='background:{color}; width:{pct}%; height:6px; border-radius:20px;'></div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# AGENT 2 — Instructional Designer Agent
# ══════════════════════════════════════════════════════════════════════════════

elif agent == "✏️ Instructional Designer Agent":

    col_sel, col_info = st.columns([1.5, 2.5])
    with col_sel:
        st.markdown('<div class="sec-header">Content Brief</div>', unsafe_allow_html=True)

        mode = st.radio("Mode", ["Use existing brief", "Enter new brief"], horizontal=True)

        if mode == "Use existing brief":
            brief_key = st.selectbox("Select brief", list(STORYBOARD_MODULES.keys()))
            brief_data = STORYBOARD_MODULES[brief_key]
            st.markdown(f"""
            <div class="agent-card" style="margin-top:12px;">
              <h3>Brief Details</h3>
              <p>👥 Audience: {brief_data['audience']}</p>
              <p>⏱ Duration: {brief_data['duration']}</p>
              <p>📦 Format: {brief_data['format']}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            brief_key = st.text_input("Module title", placeholder="e.g. Tractor Hydraulics for Dealers")
            st.text_area("Subject matter / content brief", placeholder="Paste SME notes, product specs, or a content outline here...", height=120)
            st.selectbox("Target audience", ["Engineers", "Dealers", "All employees", "Managers", "New joiners"])
            st.selectbox("Module format", ["SCORM e-learning", "Video + Quiz", "Microlearning (mobile)", "PDF job aid"])
            brief_data = STORYBOARD_MODULES[list(STORYBOARD_MODULES.keys())[0]]
            brief_key = list(STORYBOARD_MODULES.keys())[0]

        generate = st.button("🪄 Generate Storyboard", type="primary", use_container_width=True)

    with col_info:
        st.markdown('<div class="sec-header">Learning Objectives</div>', unsafe_allow_html=True)
        for obj in brief_data["objectives"]:
            st.markdown(f"<div style='font-size:0.88rem; color:#333; padding:6px 0; border-bottom:1px solid #eee;'>✅ {obj}</div>", unsafe_allow_html=True)

        if brief_data.get("wcag_flags"):
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="sec-header">♿ Accessibility Flags</div>', unsafe_allow_html=True)
            for flag in brief_data["wcag_flags"]:
                st.markdown(f"<div style='font-size:0.85rem; color:{TAFE_RED}; padding:4px 0;'>⚠️ {flag}</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f'<div class="agent-card"><h3>💡 ID Agent Note</h3><p>{brief_data["id_notes"]}</p></div>', unsafe_allow_html=True)

    st.markdown("---")

    if generate or "id_generated" in st.session_state:
        st.session_state.id_generated = True
        st.markdown(f'<div class="sec-header">Generated Storyboard — {brief_key}</div>', unsafe_allow_html=True)

        progress_bar = st.progress(0, text="Instructional Designer Agent thinking…")
        for i in range(100):
            time.sleep(0.005)
            progress_bar.progress(i + 1, text=f"Generating storyboard… {i+1}%")
        progress_bar.empty()

        for mod in brief_data["modules"]:
            seq_color = TAFE_RED if mod["seq"] == "01" else (TAFE_GREEN if mod["seq"] == "05" else TAFE_NAVY)
            st.markdown(f"""
            <div class="storyboard">
              <div style='display:flex; align-items:center; gap:12px; margin-bottom:8px;'>
                <div style='background:{seq_color}; color:white; border-radius:6px; padding:3px 10px; font-size:0.78rem; font-weight:700;'>
                  Module {mod['seq']}
                </div>
                <h4 style='margin:0; color:{TAFE_NAVY};'>{mod['title']}</h4>
                <span class='pill' style='margin-left:auto;'>{mod['type']}</span>
                <span class='pill'>{mod['duration']}</span>
              </div>
              <p><b>Narration / Interaction design:</b> {mod['narration']}</p>
              <p style='margin-top:6px; font-size:0.82rem; color:#888;'>📎 Assets required: {mod['assets']}</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown('<div class="sec-header">QA Pre-Check — Before Handoff to Media Team</div>', unsafe_allow_html=True)

        pass_count = sum(1 for _, _, passed in QA_CHECKLIST_ITEMS if passed)
        fail_count = len(QA_CHECKLIST_ITEMS) - pass_count
        st.markdown(f"""
        <div style='background:white; border-radius:10px; padding:14px 20px; margin-bottom:16px; display:flex; gap:30px; align-items:center; box-shadow:0 1px 4px rgba(0,0,0,0.05);'>
          <div><span style='font-size:1.5rem; font-weight:800; color:{TAFE_GREEN};'>{pass_count}</span> <span style='font-size:0.85rem; color:#666;'>checks passed</span></div>
          <div><span style='font-size:1.5rem; font-weight:800; color:{TAFE_RED};'>{fail_count}</span> <span style='font-size:0.85rem; color:#666;'>need attention</span></div>
          <div style='font-size:0.82rem; color:#888;'>Human review required before authoring sign-off</div>
        </div>
        """, unsafe_allow_html=True)

        categories = {}
        for cat, item, passed in QA_CHECKLIST_ITEMS:
            categories.setdefault(cat, []).append((item, passed))

        qa_cols = st.columns(2)
        for i, (cat, items) in enumerate(categories.items()):
            with qa_cols[i % 2]:
                st.markdown(f'<div style="font-size:0.82rem; font-weight:700; color:{TAFE_NAVY}; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:6px;">{cat}</div>', unsafe_allow_html=True)
                for item, passed in items:
                    icon = "✅" if passed else "❌"
                    color = "#333" if passed else TAFE_RED
                    st.markdown(f'<div style="font-size:0.84rem; color:{color}; padding:4px 0; border-bottom:1px solid #f0f0f0;">{icon} {item}</div>', unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)

        st.success("✅ Storyboard generated. Ready for content team review before authoring begins. All outputs logged to SharePoint with model version, timestamp, and prompt ID.")

# ══════════════════════════════════════════════════════════════════════════════
# AGENT 3 — Learning Campaigner Agent
# ══════════════════════════════════════════════════════════════════════════════

elif agent == "📣 Learning Campaigner Agent":

    left, right = st.columns([1.5, 2.5])

    with left:
        st.markdown('<div class="sec-header">Active Campaigns</div>', unsafe_allow_html=True)

        selected_campaign = None
        for camp in CAMPAIGN_EVENTS:
            status_color = TAFE_GREEN if camp["status"] == "Active" else ("#FFA500" if camp["status"] == "Draft" else "#888")
            if st.button(
                f"{camp['name']} · {camp['status']}",
                key=f"camp_{camp['name']}",
                use_container_width=True,
            ):
                st.session_state.selected_camp = camp["name"]

        if "selected_camp" not in st.session_state:
            st.session_state.selected_camp = CAMPAIGN_EVENTS[0]["name"]

        selected_campaign = next(c for c in CAMPAIGN_EVENTS if c["name"] == st.session_state.selected_camp)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="sec-header">Create New Campaign</div>', unsafe_allow_html=True)
        new_name = st.text_input("Campaign name", placeholder="e.g. Safety Week Sprint")
        new_trigger = st.selectbox("Trigger type", ["Date-based", "Birthday / Anniversary", "Completion milestone", "Manager-initiated", "Low engagement alert"])
        new_audience = st.selectbox("Audience", ["All employees", "Specific department", "At-risk learners", "Top learners", "Specific role"])
        if st.button("➕ Create Campaign", use_container_width=True):
            st.success(f"Campaign '{new_name}' created as Draft. AI will generate personalised nudges based on learner profiles.")

    with right:
        if selected_campaign:
            camp = selected_campaign
            status_color = TAFE_GREEN if camp["status"] == "Active" else ("#FFA500" if camp["status"] == "Draft" else "#888")

            st.markdown(f"""
            <div class="campaign-card">
              <div style='display:flex; align-items:center; gap:12px; margin-bottom:4px;'>
                <h4 style='margin:0; font-size:1.05rem;'>{camp['name']}</h4>
                <span style='background:{status_color}; color:white; border-radius:20px; padding:2px 12px; font-size:0.76rem; font-weight:700;'>{camp['status']}</span>
              </div>
              <div style='font-size:0.83rem; color:#666; margin-bottom:4px;'>🔁 Trigger: {camp['trigger']} &nbsp;·&nbsp; 👥 Reach: {camp['reach']} &nbsp;·&nbsp; 💬 {camp['channel']}</div>
              <div class='nudge-preview'>
                <div style='font-size:0.75rem; color:#999; margin-bottom:6px; font-style:normal; font-weight:600; text-transform:uppercase; letter-spacing:0.5px;'>Sample Personalised Nudge (auto-generated)</div>
                {camp['nudge']}
              </div>
            </div>
            """, unsafe_allow_html=True)

            if camp["status"] != "Draft":
                st.markdown('<div class="sec-header">Campaign Performance</div>', unsafe_allow_html=True)
                pm1, pm2, pm3 = st.columns(3)
                pm1.markdown(f'<div class="metric-tile"><div class="val">{camp["sent_30d"]:,}</div><div class="lbl">Nudges Sent (30d)</div></div>', unsafe_allow_html=True)
                pm2.markdown(f'<div class="metric-tile"><div class="val">{camp["open_rate"]}%</div><div class="lbl">Open Rate</div><div class="delta">Target: ≥50%</div></div>', unsafe_allow_html=True)
                pm3.markdown(f'<div class="metric-tile"><div class="val">{camp["start_rate"]}%</div><div class="lbl">Learning Start Rate</div><div class="delta">Target: ≥30%</div></div>', unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

            st.markdown('<div class="sec-header">Nudge Builder</div>', unsafe_allow_html=True)
            tone = st.select_slider("Tone", options=["Formal", "Professional", "Friendly", "Motivational", "Celebratory"])
            length = st.radio("Message length", ["Short (1–2 lines)", "Medium (3–4 lines)", "Full (with CTA)"], horizontal=True)

            if st.button("🔄 Regenerate Personalised Nudge", use_container_width=True):
                nudge_variants = {
                    "Birthday": {
                        "Short (1–2 lines)": "🎂 Happy Birthday! Celebrate with a 15-min learning boost — just for you.",
                        "Medium (3–4 lines)": "🎂 Happy Birthday from TAFE L&D! Today's a great day to invest in yourself. We've picked a short module aligned to your career goals — give it a try!",
                        "Full (with CTA)": f"🎂 Wishing you a wonderful Birthday! At TAFE, we believe every milestone is a chance to grow. We've personalised today's recommendation just for you based on your learning history. [Start your birthday module →] It's only 20 minutes — the best gift you can give yourself today.",
                    },
                    "Cultural": {
                        "Short (1–2 lines)": "🪔 Festival greetings! A short learning treat awaits you today.",
                        "Medium (3–4 lines)": "🪔 Warm festival wishes from TAFE L&D! May this season bring growth and learning. We've lined up a short, festive module — a gift from us to you.",
                        "Full (with CTA)": "🪔 Warm Diwali Greetings! As we celebrate the festival of lights, let's also light up our learning journeys. TAFE L&D has curated a 15-minute special for you. [Start the Diwali Learning Challenge →] Join 1,200+ colleagues who've already started today!",
                    },
                }
                default_nudge = nudge_variants.get(camp["type"], {}).get(length, camp["nudge"])
                st.markdown(f"""
                <div style='background:{TAFE_CREAM}; border-radius:10px; padding:16px; border:1px dashed {TAFE_GREEN}; margin-top:10px;'>
                  <div style='font-size:0.75rem; font-weight:700; color:{TAFE_GREEN}; margin-bottom:8px; text-transform:uppercase; letter-spacing:0.5px;'>Regenerated · {tone} · {length}</div>
                  <div style='font-size:0.9rem; color:#333; line-height:1.6;'>{default_nudge}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown('<div class="sec-header">Birthday Nudge Engine — Today\'s Queue</div>', unsafe_allow_html=True)
        today_bday = [
            ("Suresh Kumar", "Sales", "Product Knowledge Essentials", "Sent 8:02 AM", True),
            ("Anitha Rao", "Manufacturing", "Safety Compliance Refresher", "Sent 8:02 AM", True),
            ("Gopal M.", "R&D", "DIVA Pro Certification", "Pending 9:00 AM", False),
            ("Latha S.", "HR", "Leadership Foundations", "Pending 9:00 AM", False),
        ]
        for name, dept, course, status, sent in today_bday:
            icon = "✅" if sent else "🕐"
            color = TAFE_GREEN if sent else "#FFA500"
            st.markdown(f"""
            <div style='background:white; border-radius:8px; padding:10px 16px; margin-bottom:7px; display:flex; align-items:center; gap:12px; box-shadow:0 1px 3px rgba(0,0,0,0.05);'>
              <div style='font-size:1.1rem;'>{icon}</div>
              <div style='flex:1;'>
                <div style='font-weight:600; font-size:0.88rem; color:{TAFE_NAVY};'>{name} <span style='font-weight:400; color:#888;'>· {dept} 🎂</span></div>
                <div style='font-size:0.8rem; color:#888;'>Recommended: {course}</div>
              </div>
              <div style='font-size:0.8rem; color:{color}; font-weight:600;'>{status}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f'<div style="font-size:0.78rem; color:#aaa; margin-top:6px;">Nudges triggered via Power Automate · HR birthday data sync at 7:00 AM daily · Opt-out honoured · Learning history pulled from Moodle</div>', unsafe_allow_html=True)
