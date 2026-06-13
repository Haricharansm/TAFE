import streamlit as st
import time
import random

st.set_page_config(
    page_title="TAFE · AIssist",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════
# DESIGN TOKENS
# ══════════════════════════════════════════════════════
NAVY      = "#0D1B2A"
NAVY_MID  = "#162436"
NAVY_SOFT = "#1E3148"
RED       = "#C8102E"
RED_SOFT  = "#F5E6E9"
GREEN     = "#1A7A3C"
GREEN_SOFT= "#E6F4EC"
GOLD      = "#D4A017"
GOLD_SOFT = "#FBF3DC"
WHITE     = "#FAFAF8"
SLATE     = "#EDF0F4"
GREY      = "#C8CDD6"
TEXT_DARK = "#0D1B2A"
TEXT_MID  = "#4A5568"
TEXT_LITE = "#8896A8"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

html, body, [data-testid="stAppViewContainer"] {{
    font-family: 'Inter', sans-serif;
    background: {SLATE};
    color: {TEXT_DARK};
}}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{
    background: {NAVY} !important;
    border-right: none;
}}
[data-testid="stSidebar"] > div:first-child {{ padding: 0; }}
section[data-testid="stSidebar"] .stRadio label {{
    color: #8896A8 !important;
    font-size: 0.82rem !important;
}}
[data-testid="stSidebar"] .stSelectbox label {{ color: #556 !important; font-size:0.7rem !important; }}

/* ── Hide chrome ── */
#MainMenu, footer, header {{ visibility: hidden; }}
.stDeployButton {{ display: none; }}
[data-testid="stToolbar"] {{ display: none; }}

/* ── Buttons ── */
.stButton > button {{
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    border: 1.5px solid {GREY} !important;
    background: {WHITE} !important;
    color: {TEXT_DARK} !important;
    padding: 7px 14px !important;
    transition: all 0.15s ease !important;
    letter-spacing: 0.01em !important;
}}
.stButton > button:hover {{
    border-color: {RED} !important;
    color: {RED} !important;
    background: {RED_SOFT} !important;
}}

/* ── Primary button ── */
.stButton > button[kind="primary"] {{
    background: {RED} !important;
    color: white !important;
    border-color: {RED} !important;
}}
.stButton > button[kind="primary"]:hover {{
    background: #a50e26 !important;
    color: white !important;
}}

/* ── Inputs ── */
.stTextInput > div > div > input {{
    border-radius: 10px !important;
    border: 1.5px solid {GREY} !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.88rem !important;
    padding: 10px 14px !important;
    background: {WHITE} !important;
    color: {TEXT_DARK} !important;
}}
.stTextInput > div > div > input:focus {{
    border-color: {RED} !important;
    box-shadow: 0 0 0 3px rgba(200,16,46,0.08) !important;
}}

/* ── Select ── */
.stSelectbox > div > div {{
    border-radius: 10px !important;
    border: 1.5px solid {GREY} !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.88rem !important;
    background: {WHITE} !important;
}}

/* ── Radio ── */
.stRadio > div {{ gap: 4px; }}

/* ── Columns gap ── */
div[data-testid="stHorizontalBlock"] > div {{ padding: 0 5px; }}

/* ── Progress bar ── */
.stProgress > div > div > div > div {{ background: {GREEN} !important; border-radius: 99px; }}
.stProgress > div > div > div {{ background: {SLATE}; border-radius: 99px; }}

/* ── Divider ── */
hr {{ border: none; border-top: 1px solid {GREY}; margin: 16px 0; opacity: 0.5; }}

/* ── Alerts ── */
.stSuccess {{ border-radius: 10px !important; }}

/* ────────────────────────────────────────────
   COMPONENT CLASSES
──────────────────────────────────────────── */

/* Top bar */
.topbar {{
    background: linear-gradient(135deg, {NAVY} 0%, {NAVY_SOFT} 100%);
    border-radius: 14px;
    padding: 18px 28px;
    display: flex;
    align-items: center;
    gap: 20px;
    margin-bottom: 22px;
    box-shadow: 0 4px 20px rgba(13,27,42,0.15);
}}
.topbar-brand {{ display: flex; flex-direction: column; }}
.topbar-logo {{
    font-size: 1.55rem; font-weight: 900; color: {RED};
    letter-spacing: 1.5px; line-height: 1;
}}
.topbar-sub {{ font-size: 0.72rem; color: {TEXT_LITE}; margin-top: 3px; letter-spacing: 0.3px; }}
.topbar-divider {{
    width: 1px; height: 36px;
    background: rgba(255,255,255,0.12); margin: 0 4px;
}}
.topbar-title {{ font-size: 1.05rem; font-weight: 700; color: white; }}
.topbar-badge {{
    margin-left: auto;
    background: rgba(255,255,255,0.1);
    border: 1px solid rgba(255,255,255,0.15);
    color: rgba(255,255,255,0.85);
    border-radius: 99px; padding: 5px 16px;
    font-size: 0.75rem; font-weight: 600; letter-spacing: 0.3px;
    backdrop-filter: blur(8px);
}}

/* Section header */
.sec {{
    font-size: 0.7rem; font-weight: 700; color: {TEXT_LITE};
    text-transform: uppercase; letter-spacing: 1.5px;
    margin-bottom: 12px; padding-bottom: 8px;
    border-bottom: 2px solid {RED};
    display: flex; align-items: center; gap: 8px;
}}
.sec span {{ color: {RED}; font-size: 0.85rem; }}

/* Profile card */
.profile-card {{
    background: {WHITE};
    border-radius: 14px;
    padding: 20px;
    box-shadow: 0 2px 12px rgba(13,27,42,0.06);
    margin-bottom: 14px;
}}
.profile-avatar {{
    width: 48px; height: 48px;
    background: linear-gradient(135deg, {RED} 0%, #8B0020 100%);
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem; font-weight: 800; color: white;
    margin-bottom: 12px;
    flex-shrink: 0;
}}
.profile-name {{ font-size: 1rem; font-weight: 700; color: {TEXT_DARK}; }}
.profile-role {{ font-size: 0.8rem; color: {TEXT_MID}; margin-top: 2px; }}
.profile-goal {{
    font-size: 0.78rem; color: {TEXT_MID};
    background: {GOLD_SOFT}; border-radius: 8px;
    padding: 7px 10px; margin-top: 12px;
    border-left: 3px solid {GOLD};
}}

/* Metric card */
.metric-row {{ display: flex; gap: 10px; margin-bottom: 14px; }}
.metric {{
    flex: 1; background: {WHITE}; border-radius: 12px;
    padding: 14px 12px; text-align: center;
    box-shadow: 0 1px 6px rgba(13,27,42,0.05);
}}
.metric-val {{ font-size: 1.6rem; font-weight: 800; color: {TEXT_DARK}; line-height: 1; }}
.metric-val.danger {{ color: {RED}; }}
.metric-val.success {{ color: {GREEN}; }}
.metric-lbl {{ font-size: 0.72rem; color: {TEXT_LITE}; margin-top: 4px; font-weight: 500; }}

/* Progress panel */
.progress-panel {{
    background: {WHITE}; border-radius: 12px;
    padding: 16px 18px; margin-bottom: 14px;
    box-shadow: 0 1px 6px rgba(13,27,42,0.05);
}}
.progress-label {{ font-size: 0.75rem; color: {TEXT_LITE}; font-weight: 600; margin-bottom: 8px; }}
.progress-track {{
    background: {SLATE}; border-radius: 99px; height: 8px; overflow: hidden;
}}
.progress-fill {{
    height: 8px; border-radius: 99px;
    background: linear-gradient(90deg, {GREEN} 0%, #25A85A 100%);
}}
.progress-val {{ font-size: 0.88rem; font-weight: 700; color: {TEXT_DARK}; margin-top: 7px; }}

/* Pill tags */
.pill-row {{ display: flex; flex-wrap: wrap; gap: 6px; }}
.pill {{
    display: inline-flex; align-items: center; gap: 4px;
    border-radius: 99px; padding: 4px 11px;
    font-size: 0.75rem; font-weight: 600;
}}
.pill-green {{ background: {GREEN_SOFT}; color: {GREEN}; }}
.pill-red   {{ background: {RED_SOFT};   color: {RED};   }}
.pill-gold  {{ background: {GOLD_SOFT};  color: #8B6800; }}
.pill-slate {{ background: {SLATE};      color: {TEXT_MID}; }}
.pill-navy  {{ background: #E8EDF3;      color: {NAVY}; }}

/* Chat container */
.chat-wrap {{
    background: {WHITE}; border-radius: 14px;
    padding: 20px; min-height: 380px;
    box-shadow: 0 2px 12px rgba(13,27,42,0.06);
    display: flex; flex-direction: column; gap: 14px;
    margin-bottom: 14px;
}}

/* Chat bubble — AI */
.bubble-ai {{
    display: flex; gap: 10px; align-items: flex-start;
}}
.bubble-ai-avatar {{
    width: 32px; height: 32px; border-radius: 10px; flex-shrink: 0;
    background: linear-gradient(135deg, {RED} 0%, #8B0020 100%);
    display: flex; align-items: center; justify-content: center;
    font-size: 0.75rem; font-weight: 800; color: white;
}}
.bubble-ai-content {{
    background: {SLATE}; border-radius: 4px 14px 14px 14px;
    padding: 12px 16px; max-width: 85%;
}}
.bubble-ai-label {{
    font-size: 0.68rem; font-weight: 700; color: {RED};
    letter-spacing: 0.5px; text-transform: uppercase; margin-bottom: 5px;
}}
.bubble-ai-text {{ font-size: 0.87rem; color: {TEXT_DARK}; line-height: 1.6; }}

/* Chat bubble — User */
.bubble-user {{
    display: flex; justify-content: flex-end;
}}
.bubble-user-content {{
    background: linear-gradient(135deg, {NAVY} 0%, {NAVY_SOFT} 100%);
    color: white; border-radius: 14px 4px 14px 14px;
    padding: 11px 16px; max-width: 75%;
    font-size: 0.87rem; line-height: 1.5;
}}

/* Quick prompt chips */
.chip-row {{ display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 12px; }}

/* Storyboard module card */
.sb-card {{
    background: {WHITE}; border-radius: 12px;
    border: 1px solid #E4E8EE;
    padding: 16px 20px; margin-bottom: 10px;
}}
.sb-seq {{
    display: inline-flex; align-items: center; justify-content: center;
    width: 28px; height: 28px; border-radius: 8px;
    font-size: 0.75rem; font-weight: 800; color: white;
    flex-shrink: 0;
}}
.sb-title {{ font-size: 0.95rem; font-weight: 700; color: {TEXT_DARK}; }}
.sb-type {{ font-size: 0.75rem; color: {TEXT_MID}; margin-top: 1px; }}
.sb-narration {{ font-size: 0.84rem; color: {TEXT_MID}; line-height: 1.6; margin-top: 8px; }}
.sb-assets {{
    font-size: 0.78rem; color: {TEXT_LITE}; margin-top: 8px;
    padding-top: 8px; border-top: 1px solid #EEF0F4;
}}

/* QA check item */
.qa-item {{
    display: flex; align-items: flex-start; gap: 10px;
    font-size: 0.83rem; padding: 7px 0;
    border-bottom: 1px solid #F0F2F6; color: {TEXT_DARK};
}}
.qa-pass {{ color: {GREEN}; font-weight: 700; font-size: 0.9rem; flex-shrink:0; }}
.qa-fail {{ color: {RED};   font-weight: 700; font-size: 0.9rem; flex-shrink:0; }}

/* Campaign card */
.camp-card {{
    background: {WHITE}; border-radius: 14px;
    padding: 18px 20px; margin-bottom: 12px;
    box-shadow: 0 2px 10px rgba(13,27,42,0.06);
    border-top: 4px solid {GREEN};
    cursor: pointer; transition: box-shadow 0.15s;
}}
.camp-card:hover {{ box-shadow: 0 4px 18px rgba(13,27,42,0.1); }}
.camp-title {{ font-size: 0.95rem; font-weight: 700; color: {TEXT_DARK}; }}
.camp-meta  {{ font-size: 0.78rem; color: {TEXT_LITE}; margin-top: 3px; }}
.nudge-box {{
    background: {SLATE}; border-radius: 10px;
    padding: 13px 15px; margin-top: 12px;
    font-size: 0.84rem; color: {TEXT_MID}; line-height: 1.65;
    border-left: 3px solid {GREEN};
    font-style: italic;
}}

/* Team member row */
.team-row {{
    background: {WHITE}; border-radius: 10px;
    padding: 11px 16px; margin-bottom: 7px;
    display: flex; align-items: center; gap: 12px;
    box-shadow: 0 1px 4px rgba(13,27,42,0.04);
}}
.team-avatar {{
    width: 34px; height: 34px; border-radius: 9px;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.78rem; font-weight: 800; color: white; flex-shrink: 0;
}}
.team-name {{ font-size: 0.87rem; font-weight: 600; color: {TEXT_DARK}; }}
.team-role {{ font-size: 0.75rem; color: {TEXT_LITE}; }}
.team-bar-track {{ background: #EEF0F4; border-radius: 99px; height: 5px; margin-top: 5px; }}
.team-bar-fill  {{ height: 5px; border-radius: 99px; }}

/* Heatmap bar */
.hm-row {{
    background: {WHITE}; border-radius: 10px;
    padding: 10px 14px; margin-bottom: 7px;
    box-shadow: 0 1px 3px rgba(13,27,42,0.04);
}}
.hm-name {{ font-size: 0.84rem; font-weight: 600; color: {TEXT_DARK}; }}
.hm-pct  {{ font-size: 0.84rem; font-weight: 700; }}

/* Birthday queue row */
.bday-row {{
    background: {WHITE}; border-radius: 10px;
    padding: 10px 16px; margin-bottom: 7px;
    display: flex; align-items: center; gap: 12px;
    box-shadow: 0 1px 3px rgba(13,27,42,0.04);
}}
.bday-avatar {{
    width: 36px; height: 36px; border-radius: 10px;
    background: linear-gradient(135deg, {GOLD} 0%, #a07800 100%);
    display: flex; align-items: center; justify-content: center;
    font-size: 0.78rem; font-weight: 800; color: white; flex-shrink: 0;
}}
.bday-name {{ font-size: 0.87rem; font-weight: 600; color: {TEXT_DARK}; }}
.bday-course {{ font-size: 0.75rem; color: {TEXT_LITE}; }}

/* Stat mini badge */
.stat-mini {{
    display: inline-flex; flex-direction: column;
    align-items: center; background: {SLATE};
    border-radius: 10px; padding: 8px 14px;
}}
.stat-mini-val {{ font-size: 1.2rem; font-weight: 800; color: {TEXT_DARK}; }}
.stat-mini-lbl {{ font-size: 0.68rem; color: {TEXT_LITE}; font-weight: 500; }}

/* Sidebar nav item */
.nav-item {{
    display: flex; align-items: center; gap: 10px;
    padding: 10px 16px; border-radius: 10px;
    cursor: pointer; transition: background 0.15s;
    color: #8896A8; font-size: 0.85rem; font-weight: 500;
    margin-bottom: 3px;
}}
.nav-item:hover {{ background: rgba(255,255,255,0.06); color: white; }}
.nav-item.active {{ background: rgba(200,16,46,0.18); color: white; border-left: 3px solid {RED}; }}

/* Info footer */
.info-footer {{
    font-size: 0.73rem; color: {TEXT_LITE};
    margin-top: 8px; line-height: 1.6;
    padding: 10px 0;
    border-top: 1px solid rgba(200,205,214,0.4);
}}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# DATA
# ══════════════════════════════════════════════════════
LEARNERS = {
    "Arjun Mehta — Engineer, Powertrain": {
        "initials": "AM", "role": "Engineer", "dept": "Powertrain", "level": "Mid-level",
        "completed": 14, "in_progress": 3, "overdue": 1,
        "completion_rate": 72, "hours_ytd": 38,
        "skills": ["Hydraulics", "Engine Calibration", "Quality Standards"],
        "gaps": ["Safety Compliance", "Advanced CAD"],
        "recommended": [
            ("ISO 9001 Quality Management for Engineers", "Compliance", "2h 30m"),
            ("Advanced CAD Design Principles", "Technical", "4h"),
            ("Lean Manufacturing Fundamentals", "Operations", "3h"),
        ],
        "career_goal": "Senior Design Engineer",
    },
    "Priya Venkat — Manager, Sales": {
        "initials": "PV", "role": "Manager", "dept": "Sales", "level": "Senior",
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
        "team_size": 12, "team_completion": 68,
    },
}

BRIEFS = {
    "TAFE DIVA Pro — New Product Introduction": {
        "audience": "Dealer network, Sales Engineers",
        "duration": "45 min", "format": "SCORM + Video",
        "objectives": [
            "Describe key differentiators of DIVA Pro vs. previous generation",
            "Explain the 4WD transmission mechanism and maintenance schedule",
            "Handle common dealer FAQs with confidence",
        ],
        "modules": [
            {"seq": "01", "color": RED,   "title": "Welcome & Product Overview",     "type": "Intro + Hero Video",     "narration": "Open with DIVA Pro hero shot. Narrator introduces the product generation. Transition to feature comparison table vs DIVA Standard. Tone: energetic, confident.", "assets": "Hero video (60s), comparison graphic"},
            {"seq": "02", "color": NAVY,  "title": "Engine & Powertrain Deep Dive",  "type": "Explainer + 3D Diagram", "narration": "Animated 3D cutaway of 50HP engine with callout labels: turbocharged intake, dual-stage filtration, Agri-ECU. Knowledge check: drag-and-drop component identification.", "assets": "3D engine model (Unity), labeled diagram PNG"},
            {"seq": "03", "color": NAVY,  "title": "4WD Transmission & Field Use",   "type": "Branching Scenario",    "narration": "Farmer selects terrain type (paddy, upland, orchard) — learner chooses correct gear range and 4WD mode. Wrong answers show consequences with corrective feedback.", "assets": "Branching scenario (Articulate), terrain photos"},
            {"seq": "04", "color": GREEN, "title": "Dealer Q&A Simulator",           "type": "AI Role-Play Practice", "narration": "AI-powered simulation: customer asks pricing, John Deere comparison, warranty. Learner types responses; AI scores on accuracy and confidence language.", "assets": "AIssist Q&A integration"},
            {"seq": "05", "color": GOLD,  "title": "Assessment & Certification",     "type": "Adaptive Quiz + Badge",  "narration": "20-question adaptive quiz. Pass mark 80%. On pass: DIVA Pro Certified digital badge issued to Moodle profile. On fail: targeted remediation loop.", "assets": "Quiz bank (40 Qs), badge graphic"},
        ],
        "wcag": ["Ensure all diagrams include ALT text", "Avoid red/green-only colour coding for accessibility"],
        "notes": "Tone: energetic and confident. All narration scripts require Product team sign-off before voice recording. Legal review of warranty language required.",
    },
    "Safety Compliance — Working at Height (Mandatory Annual)": {
        "audience": "All plant and shop-floor employees",
        "duration": "30 min", "format": "SCORM e-learning",
        "objectives": [
            "Identify hazardous situations requiring fall protection",
            "Apply the hierarchy of controls for working at height",
            "Complete the mandatory compliance acknowledgment",
        ],
        "modules": [
            {"seq": "01", "color": RED,   "title": "Why Safety Matters at TAFE",     "type": "CEO Video + Acknowledgment", "narration": "CEO message (2 min). Key stats: 0 LTI target. Anonymised near-miss story for emotional hook. Learner clicks 'I commit to safe practices' to proceed.", "assets": "CEO video, acknowledgment widget"},
            {"seq": "02", "color": NAVY,  "title": "Spot the Hazard",               "type": "360° Hotspot Interaction",   "narration": "360° workshop scene. Learner clicks on hazards: 3 of 8 hotspots are correct (unsecured ladder, tool without anchor, no harness). Feedback per click.", "assets": "360° scene photo, hotspot config"},
            {"seq": "03", "color": NAVY,  "title": "Hierarchy of Controls",         "type": "Drag-and-Drop",              "narration": "Pyramid diagram. Learner drags 6 control types to correct level (Elimination → PPE). Animated reveal on completion.", "assets": "Hierarchy diagram, drag-drop widget"},
            {"seq": "04", "color": GREEN, "title": "Compliance Assessment",         "type": "Graded Quiz (100% required)", "narration": "15 questions, 100% pass required. Unlimited attempts. Completion auto-records in Moodle for HR audit trail.", "assets": "Question bank (30 Qs, randomised)"},
        ],
        "wcag": ["All videos require closed captions", "Hotspot targets must be keyboard-navigable"],
        "notes": "Mandatory course — zero tolerance for gamification that trivialises safety. Tone: serious, respectful. Legal review of compliance language required before publish.",
    },
}

QA_ITEMS = [
    ("Visual",        "Fonts match TAFE brand guide (Inter body, TAFE Red headers)",     True),
    ("Visual",        "Colour palette compliant — no unapproved hex values",              True),
    ("Visual",        "Logo usage correct — not distorted, on approved backgrounds",      True),
    ("Instructional", "Learning objectives stated on opening screen",                     True),
    ("Instructional", "Each objective addressed by at least one activity",                True),
    ("Instructional", "Knowledge checks present every 10 minutes",                        False),
    ("Accessibility", "All images have descriptive ALT text",                             False),
    ("Accessibility", "Colour contrast ratio ≥ 4.5:1 for body text",                     True),
    ("Accessibility", "Videos include closed captions",                                   False),
    ("Technical",     "SCORM package tested in Moodle staging",                           True),
    ("Technical",     "Module completes on pass of final assessment",                     True),
    ("Technical",     "Progress saved on mid-module exit",                                True),
]

CAMPAIGNS = [
    {
        "name": "Birthday Learning Nudge", "icon": "🎂", "type": "Birthday",
        "trigger": "Daily · 8:00 AM", "reach": "~12 employees/day",
        "channel": "Microsoft Teams", "status": "Active",
        "sent": 342, "open_rate": 67, "start_rate": 41,
        "nudge": "Hi {name}! 🎂 Happy Birthday from TAFE L&D! Today's a great day to invest 20 minutes in yourself — we've picked a short module that fits your role perfectly. Celebrate your growth! 🌾",
        "color": GOLD,
    },
    {
        "name": "World Book Day Sprint", "icon": "📚", "type": "Cultural",
        "trigger": "April 23 (annual)", "reach": "All 4,200 employees",
        "channel": "Teams + Email", "status": "Completed",
        "sent": 4200, "open_rate": 72, "start_rate": 38,
        "nudge": "Hi {name}! Today is World Book Day 📚 — learning is at the heart of TAFE's culture. We've curated a 30-minute reading challenge from our knowledge library. Join 847 colleagues who've already started today!",
        "color": GREEN,
    },
    {
        "name": "Farmer's Day Learning Sprint", "icon": "🚜", "type": "Brand",
        "trigger": "December 23 (annual)", "reach": "All employees",
        "channel": "Teams + Moodle Banner", "status": "Draft",
        "sent": 0, "open_rate": 0, "start_rate": 0,
        "nudge": "Happy Farmer's Day! 🌾 As TAFE employees, we celebrate the farmers we serve every day. This week: complete one module from our Product Knowledge series and earn a special Farmer's Day badge.",
        "color": NAVY,
    },
    {
        "name": "Diwali Learning Celebration", "icon": "🪔", "type": "Cultural",
        "trigger": "Diwali · November", "reach": "India offices · 3,100",
        "channel": "Microsoft Teams", "status": "Active",
        "sent": 1840, "open_rate": 81, "start_rate": 55,
        "nudge": "Diwali Greetings! 🪔 May this festival of lights also light up your learning journey. We've lined up a short 15-minute module — a gift from L&D to you. Wishing you and your family a joyful Diwali!",
        "color": RED,
    },
]

BDAY_QUEUE = [
    ("Suresh Kumar",  "SK", "Sales",           "Product Knowledge Essentials",      "Sent · 8:02 AM",   True),
    ("Anitha Rao",    "AR", "Manufacturing",   "Safety Compliance Refresher",        "Sent · 8:02 AM",   True),
    ("Gopal M.",      "GM", "R&D",             "DIVA Pro Certification",             "Pending · 9:00 AM", False),
    ("Latha S.",      "LS", "HR",              "Leadership Foundations",             "Pending · 9:00 AM", False),
]

TEAM_MEMBERS = [
    ("Suresh Kumar",  "SK", "Sales Executive",  92, "On Track"),
    ("Meena Raj",     "MR", "Sales Executive",  78, "On Track"),
    ("Anand P.",      "AP", "Area Manager",     65, "At Risk"),
    ("Divya S.",      "DS", "Sales Executive",  55, "At Risk"),
    ("Karthik M.",    "KM", "Key Accounts",     30, "Overdue"),
    ("Raj Patel",     "RP", "Sales Executive",  82, "On Track"),
]


def status_color(s):
    return {
        "On Track": GREEN, "At Risk": "#D97706", "Overdue": RED
    }.get(s, GREY)


def avatar_color(initials):
    colors = [RED, GREEN, NAVY_SOFT, "#7C3AED", "#0891B2", "#059669"]
    return colors[sum(ord(c) for c in initials) % len(colors)]


# ══════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(f"""
    <div style="padding: 24px 20px 20px;">
      <div style="font-size:1.5rem; font-weight:900; color:{RED}; letter-spacing:2px;">TAFE</div>
      <div style="font-size:0.72rem; color:#556; margin-top:2px; font-weight:500; letter-spacing:0.3px;">AI(ssist) · L&D Platform</div>
    </div>
    <div style="height:1px; background:rgba(255,255,255,0.07); margin: 0 20px 20px;"></div>
    <div style="padding: 0 12px; font-size:0.68rem; font-weight:700; color:#3A4A5A; text-transform:uppercase; letter-spacing:1.5px; margin-bottom:10px;">Agents</div>
    """, unsafe_allow_html=True)

    agent = st.radio(
        "agent",
        ["🎓  Learner Assistant + AI Coach",
         "✏️  Instructional Designer",
         "📣  Learning Campaigner"],
        label_visibility="collapsed",
    )

    st.markdown(f"""
    <div style="height:1px; background:rgba(255,255,255,0.07); margin: 20px 20px;"></div>
    <div style="padding: 0 20px;">
      <div style="font-size:0.68rem; font-weight:700; color:#3A4A5A; text-transform:uppercase; letter-spacing:1.5px; margin-bottom:12px;">Platform</div>
      <div style="font-size:0.79rem; color:#6A7A8A; line-height:2.1;">
        <span style="color:{GREEN}; font-size:0.6rem;">●</span>&nbsp; Azure AI Foundry<br>
        <span style="color:{GREEN}; font-size:0.6rem;">●</span>&nbsp; Moodle LMS connector<br>
        <span style="color:{GREEN}; font-size:0.6rem;">●</span>&nbsp; Entra ID guardrails<br>
        <span style="color:{GREEN}; font-size:0.6rem;">●</span>&nbsp; R&D access controls<br>
        <span style="color:#D97706; font-size:0.6rem;">●</span>&nbsp; Analytics (Phase 2)
      </div>
    </div>
    <div style="position:absolute; bottom:24px; left:0; right:0; padding:0 20px;">
      <div style="font-size:0.7rem; color:#3A4A5A; border-top:1px solid rgba(255,255,255,0.06); padding-top:14px; line-height:1.9;">
        Powered by Saxon · Microsoft Azure<br>
        AIssist V2 · <span style="color:{RED};">Prototype · May 2026</span>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════
def topbar(title, subtitle):
    st.markdown(f"""
    <div class="topbar">
      <div class="topbar-brand">
        <div class="topbar-logo">TAFE · AI(ssist)</div>
        <div class="topbar-sub">{subtitle}</div>
      </div>
      <div class="topbar-divider"></div>
      <div class="topbar-title">{title}</div>
      <div class="topbar-badge">🌾 &nbsp;L&D Platform</div>
    </div>
    """, unsafe_allow_html=True)


def sec_header(icon, label):
    st.markdown(f'<div class="sec"><span>{icon}</span>{label}</div>', unsafe_allow_html=True)


def render_chat(messages):
    bubbles = ""
    for role, text in messages:
        text_safe = (text
            .replace("**", "<b>", 1).replace("**", "</b>", 1)
            .replace("**", "<b>", 1).replace("**", "</b>", 1)
            .replace("**", "<b>", 1).replace("**", "</b>", 1)
            .replace("**", "<b>", 1).replace("**", "</b>", 1)
            .replace("**", "<b>", 1).replace("**", "</b>", 1)
            .replace("\n\n", "<br><br>").replace("\n", "<br>"))
        if role == "ai":
            bubbles += f"""
            <div class="bubble-ai">
              <div class="bubble-ai-avatar">AI</div>
              <div class="bubble-ai-content">
                <div class="bubble-ai-label">TAFE AI Coach</div>
                <div class="bubble-ai-text">{text_safe}</div>
              </div>
            </div>"""
        else:
            bubbles += f'<div class="bubble-user"><div class="bubble-user-content">{text_safe}</div></div>'
    st.markdown(f'<div class="chat-wrap">{bubbles}</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# AGENT 1 — LEARNER ASSISTANT + AI COACH
# ══════════════════════════════════════════════════════
if "🎓" in agent:
    topbar("Learner Assistant + AI Coach", "UC-4 · Strategic POC · Phase 1 Flagship")

    rc1, rc2, _ = st.columns([1.2, 1.6, 1.5])
    with rc1:
        role_view = st.selectbox("View as", ["Learner", "Manager", "Business Head"])
    with rc2:
        if role_view == "Learner":
            sel = st.selectbox("Learner", list(LEARNERS.keys()))
        elif role_view == "Manager":
            sel = "Priya Venkat — Manager, Sales"
        else:
            sel = None

    st.markdown("---")

    # ── LEARNER VIEW ──────────────────────────────────
    if role_view == "Learner":
        p = LEARNERS[sel]
        left, right = st.columns([1, 1.8])

        with left:
            sec_header("👤", "My Learning Profile")
            name_short = sel.split("—")[0].strip()

            st.markdown(f"""
            <div class="profile-card">
              <div style="display:flex; align-items:center; gap:14px; margin-bottom:12px;">
                <div class="profile-avatar">{p['initials']}</div>
                <div>
                  <div class="profile-name">{name_short}</div>
                  <div class="profile-role">{p['role']} · {p['dept']} · {p['level']}</div>
                </div>
              </div>
              <div class="profile-goal">🎯 &nbsp;Target role: <b>{p['career_goal']}</b></div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="metric-row">
              <div class="metric">
                <div class="metric-val success">{p['completed']}</div>
                <div class="metric-lbl">Completed</div>
              </div>
              <div class="metric">
                <div class="metric-val">{p['in_progress']}</div>
                <div class="metric-lbl">In Progress</div>
              </div>
              <div class="metric">
                <div class="metric-val {'danger' if p['overdue'] > 0 else 'success'}">{p['overdue']}</div>
                <div class="metric-lbl">Overdue</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="progress-panel">
              <div class="progress-label">Course Completion · YTD</div>
              <div class="progress-track">
                <div class="progress-fill" style="width:{p['completion_rate']}%;"></div>
              </div>
              <div class="progress-val">{p['completion_rate']}% &nbsp;·&nbsp; {p['hours_ytd']}h logged</div>
            </div>
            """, unsafe_allow_html=True)

            sec_header("✅", "Current Skills")
            pills = "".join([f'<span class="pill pill-green">✓ {s}</span>' for s in p["skills"]])
            st.markdown(f'<div class="pill-row" style="margin-bottom:16px;">{pills}</div>', unsafe_allow_html=True)

            sec_header("🎯", "Skill Gaps")
            pills_g = "".join([f'<span class="pill pill-red">↑ {s}</span>' for s in p["gaps"]])
            st.markdown(f'<div class="pill-row">{pills_g}</div>', unsafe_allow_html=True)

        with right:
            sec_header("🤖", "AI Learning Coach")

            key = f"lc_{sel}"
            if key not in st.session_state:
                first_name = name_short.split()[0]
                st.session_state[key] = [
                    ("ai", f"Hi {first_name}! 👋 I'm your TAFE Learning Coach. I can see you have **{p['overdue']} overdue module** and your completion rate is **{p['completion_rate']}%** this quarter.\n\nHere's what I'd suggest tackling first — want me to walk you through your top recommendations?")
                ]

            render_chat(st.session_state[key])

            # Quick prompts
            qc1, qc2, qc3 = st.columns(3)
            prompts = [
                ("Show recommendations", qc1),
                ("What's overdue?",       qc2),
                ("Build my learning plan", qc3),
            ]
            for label, col in prompts:
                if col.button(label, use_container_width=True, key=f"qp_{label}_{sel}"):
                    first_name = name_short.split()[0]
                    st.session_state[key].append(("user", label))
                    if "recommend" in label.lower():
                        recs = p["recommended"]
                        rec_lines = "\n".join([f"**{i+1}. {r[0]}** — {r[1]} · {r[2]}" for i, r in enumerate(recs)])
                        reply = f"Here are your top 3 personalised recommendations, based on your role and skill gaps:\n\n{rec_lines}\n\nWould you like to enrol in the first one?"
                    elif "overdue" in label.lower():
                        reply = f"You have **1 overdue module**: **{p['gaps'][0]}**. It was due 12 days ago.\n\nI can block 2 hours in your Teams calendar this week to clear it. Want me to do that?"
                    else:
                        reply = f"Great idea, {first_name}! Based on your goal of becoming a **{p['career_goal']}**, here's a 90-day sprint:\n\n**Month 1:** Clear your overdue module + 2 foundational courses.\n**Month 2:** Tackle your top gap — **{p['gaps'][-1]}**.\n**Month 3:** One stretch course aligned to your next role.\n\nShall I add these to your Moodle learning path?"
                    st.session_state[key].append(("ai", reply))
                    st.rerun()

            user_q = st.text_input("Ask your AI Coach anything…", placeholder="Which course should I do next?", key=f"li_{sel}")
            if st.button("Send", key=f"ls_{sel}") and user_q:
                first_name = name_short.split()[0]
                st.session_state[key].append(("user", user_q))
                reply = f"Based on your profile, I'd recommend starting with **{p['recommended'][0][0]}** — it directly addresses your gap in **{p['gaps'][-1]}** and is only {p['recommended'][0][2]} long. Want me to enrol you?"
                st.session_state[key].append(("ai", reply))
                st.rerun()

            st.markdown(f'<div class="info-footer">All recommendations grounded in your Moodle records · Source citations included · Human review on all enrolments · Audit trail active</div>', unsafe_allow_html=True)

    # ── MANAGER VIEW ──────────────────────────────────
    elif role_view == "Manager":
        p = LEARNERS["Priya Venkat — Manager, Sales"]
        sec_header("📊", "Team Dashboard — Priya Venkat · Sales · 12 Direct Reports")

        m1, m2, m3, m4 = st.columns(4)
        for col, val, lbl, delta, dcolor in [
            (m1, "68%",  "Team Completion",     "▲ 9% vs. last quarter", GREEN),
            (m2, "8",    "Overdue (team)",       "2 critical — act now",  RED),
            (m3, "47h",  "Avg Hours YTD",        "▲ 6h vs. last quarter", GREEN),
            (m4, "3/12", "On Track for Goals",   "review recommended",    GOLD),
        ]:
            col.markdown(f"""
            <div class="metric" style="border-top: 3px solid {dcolor}; padding: 16px 12px;">
              <div class="metric-val" style="color:{dcolor};">{val}</div>
              <div class="metric-lbl">{lbl}</div>
              <div style="font-size:0.72rem; color:{dcolor}; font-weight:600; margin-top:3px;">{delta}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        tl, tr = st.columns([1.1, 1.4])

        with tl:
            sec_header("👥", "Team Members")
            for name, initials, role_t, pct, status in TEAM_MEMBERS:
                sc = status_color(status)
                ac = avatar_color(initials)
                st.markdown(f"""
                <div class="team-row">
                  <div class="team-avatar" style="background:{ac};">{initials}</div>
                  <div style="flex:1; min-width:0;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                      <div class="team-name">{name}</div>
                      <span class="pill" style="background:{sc}18; color:{sc}; font-size:0.7rem;">{status}</span>
                    </div>
                    <div class="team-role">{role_t}</div>
                    <div class="team-bar-track">
                      <div class="team-bar-fill" style="width:{pct}%; background:{sc};"></div>
                    </div>
                  </div>
                  <div style="font-size:0.85rem; font-weight:700; color:{sc}; min-width:32px; text-align:right;">{pct}%</div>
                </div>
                """, unsafe_allow_html=True)

        with tr:
            sec_header("🤖", "Manager AI Coach")
            if "mc_chat" not in st.session_state:
                st.session_state.mc_chat = [("ai", "Hi Priya! Your team's completion is **68%** — up 9 points this quarter. 🎉\n\nHowever, **Karthik M.** is critically overdue on 3 mandatory modules. I can draft a personalised nudge to him, or escalate to HR. What would you like to do?")]
            render_chat(st.session_state.mc_chat)

            nc1, nc2 = st.columns(2)
            if nc1.button("Nudge Karthik", use_container_width=True):
                st.session_state.mc_chat.append(("user", "Send nudge to Karthik"))
                st.session_state.mc_chat.append(("ai", "Done! ✅ A personalised Teams message is queued for Karthik at 9 AM tomorrow:\n\n*'Hi Karthik — I've noticed 3 overdue modules including Safety Compliance. I've cleared 2 hours in your calendar this Thursday. Let's get these done — Priya'*\n\nI'll notify you when he completes."))
                st.rerun()
            if nc2.button("Full team report", use_container_width=True):
                st.session_state.mc_chat.append(("user", "Give me the full team report"))
                st.session_state.mc_chat.append(("ai", "**Team Summary — Sales · Q2 FY26**\n\nOn Track (≥75%): Suresh, Meena, Raj — 3 of 12\nAt Risk (50–74%): Anand, Divya — need 1:1 check-in\nCritical (<50%): Karthik — mandatory escalation recommended\n\nTop gap across team: **AI for Sales Leaders** — 9 of 12 not yet enrolled."))
                st.rerun()

            mi = st.text_input("Ask about your team…", placeholder="Who needs my attention most?", key="mc_in")
            if st.button("Ask", key="mc_send") and mi:
                st.session_state.mc_chat.append(("user", mi))
                st.session_state.mc_chat.append(("ai", "**Karthik M.** and **Divya S.** need the most attention. Karthik has 3 overdue mandatory modules (30% completion). Divya is at risk with 55% — trending down. I'd suggest 1:1 check-ins with both alongside the automated nudge already queued for Karthik."))
                st.rerun()

    # ── LEADERSHIP VIEW ───────────────────────────────
    else:
        sec_header("🏢", "Executive Analytics — Organisation · 4,200 Employees")
        st.markdown('<span class="pill pill-red">🔒 Leadership Access</span>&nbsp;<span class="pill pill-gold">⚡ R&D Confidential Gated</span>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        e1, e2, e3, e4 = st.columns(4)
        for col, val, lbl, delta, dc in [
            (e1, "54%",    "Org Completion",       "▲ 11% vs. H1",      GREEN),
            (e2, "6,840h", "Learning Hours YTD",   "across all functions", NAVY),
            (e3, "3",      "Critical Gaps",         "safety compliance",  RED),
            (e4, "92%",    "NPI Readiness",         "DIVA Pro launch",    GOLD),
        ]:
            col.markdown(f"""
            <div class="metric" style="border-top:3px solid {dc}; padding:16px 12px;">
              <div class="metric-val" style="color:{dc};">{val}</div>
              <div class="metric-lbl">{lbl}</div>
              <div style="font-size:0.72rem; color:{dc}; font-weight:600; margin-top:3px;">{delta}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        el, er = st.columns([1.6, 1])

        with el:
            sec_header("💬", "Conversational Analytics")
            if "ec_chat" not in st.session_state:
                st.session_state.ec_chat = [("ai", "Good morning! Your organisation's learning adoption is at **54%** — 11 points up from H1.\n\n**NPI readiness for DIVA Pro: 92%** — 8 engineers yet to complete product certification.\n\nWould you like a breakdown by function, or an action plan for the remaining 8?")]
            render_chat(st.session_state.ec_chat)

            eq1, eq2, eq3 = st.columns(3)
            for label, col, resp in [
                ("Best learners", eq1, "Your top 5 learners this quarter:\n\n**Arun T.** — 98% · 42h\n**Sneha G.** — 96% · 38h\n**Vikram N.** — 94% · 35h\n**Preethi A.** — 92% · 33h\n**Mohan R.** — 90% · 31h\n\nAll 5 are in Advanced Engineering — 12 points above org average."),
                ("Function gaps",  eq2, "3 functions show critical learning gaps:\n\n**Field Testing** — 38% (safety modules overdue)\n**Electronics & Embedded** — 44% (NPI cert at risk)\n**Prototyping** — 52% (manageable)\n\nRecommend a targeted sprint for Field Testing this month."),
                ("NPI readiness",  eq3, "**DIVA Pro NPI Readiness: 92%**\n220 of 240 R&D engineers certified. 8 remaining engineers are in Field Testing — all have been nudged.\n\nProjected 100% by June 28. **Risk: LOW.** No launch readiness concerns."),
            ]:
                if col.button(label, use_container_width=True, key=f"eq_{label}"):
                    st.session_state.ec_chat.append(("user", label))
                    st.session_state.ec_chat.append(("ai", resp))
                    st.rerun()

            ex = st.text_input("Query the analytics engine…", placeholder="How much capability learning has R&D done this quarter?", key="ex_in")
            if st.button("Query", key="ex_send") and ex:
                st.session_state.ec_chat.append(("user", ex))
                h = random.randint(1200, 1800)
                up = random.randint(10, 20)
                st.session_state.ec_chat.append(("ai", f"R&D completed **{h:,} capability learning hours** this quarter — a **{up}% increase** vs. Q4 FY25.\n\nTop areas: Product Engineering (840h), Safety (320h), Leadership (210h).\nTrending up: AI & Digital Tools **+68% YoY**."))
                st.rerun()

        with er:
            sec_header("🗺️", "Function Heatmap")
            hm = [
                ("Advanced Engineering",      88),
                ("R&D Management",            91),
                ("Quality Assurance",         77),
                ("Prototyping",               52),
                ("Electronics & Embedded",    44),
                ("Field Testing",             38),
            ]
            for name, pct in hm:
                c = GREEN if pct >= 75 else ("#D97706" if pct >= 50 else RED)
                st.markdown(f"""
                <div class="hm-row">
                  <div style="display:flex; justify-content:space-between; margin-bottom:5px;">
                    <div class="hm-name">{name}</div>
                    <div class="hm-pct" style="color:{c};">{pct}%</div>
                  </div>
                  <div class="team-bar-track">
                    <div class="team-bar-fill" style="width:{pct}%; background:linear-gradient(90deg, {c}99, {c});"></div>
                  </div>
                </div>
                """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# AGENT 2 — INSTRUCTIONAL DESIGNER
# ══════════════════════════════════════════════════════
elif "✏️" in agent:
    topbar("Instructional Designer Agent", "UC-1 · Quick Win · Phase 1 · Fills the role gap")

    bc1, bc2 = st.columns([1.2, 2.4])
    with bc1:
        sec_header("📋", "Content Brief")
        mode = st.radio("Input mode", ["Existing brief", "New brief"], horizontal=True, label_visibility="collapsed")
        if mode == "Existing brief":
            brief_key = st.selectbox("Select brief", list(BRIEFS.keys()))
        else:
            brief_key = list(BRIEFS.keys())[0]
            st.text_input("Module title", placeholder="e.g. Tractor Hydraulics for Dealers")
            st.text_area("Subject matter / SME notes", placeholder="Paste content outline or product specs…", height=100)
            st.selectbox("Target audience", ["Engineers", "Dealers", "All employees", "Managers"])
            st.selectbox("Format", ["SCORM e-learning", "Video + Quiz", "Microlearning", "PDF job aid"])

        b = BRIEFS[brief_key]
        st.markdown(f"""
        <div class="profile-card" style="margin-top:14px;">
          <div style="font-size:0.75rem; font-weight:700; color:{TEXT_LITE}; text-transform:uppercase; letter-spacing:1px; margin-bottom:10px;">Brief Details</div>
          <div style="font-size:0.84rem; color:{TEXT_DARK}; line-height:2.1;">
            👥 &nbsp;<b>Audience:</b> {b['audience']}<br>
            ⏱ &nbsp;<b>Duration:</b> {b['duration']}<br>
            📦 &nbsp;<b>Format:</b> {b['format']}
          </div>
        </div>
        """, unsafe_allow_html=True)

        generate = st.button("🪄  Generate Storyboard", type="primary", use_container_width=True)

    with bc2:
        sec_header("🎯", "Learning Objectives")
        for obj in b["objectives"]:
            st.markdown(f"""
            <div style="display:flex; gap:10px; align-items:flex-start; padding:8px 0; border-bottom:1px solid #EEF0F4; font-size:0.86rem; color:{TEXT_DARK};">
              <span style="color:{GREEN}; font-weight:700; flex-shrink:0;">✓</span>
              <span>{obj}</span>
            </div>
            """, unsafe_allow_html=True)

        if b["wcag"]:
            st.markdown("<br>", unsafe_allow_html=True)
            sec_header("♿", "Accessibility Requirements")
            for flag in b["wcag"]:
                st.markdown(f'<div style="font-size:0.84rem; color:{RED}; padding:5px 0;">⚠️ &nbsp;{flag}</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="profile-card" style="border-left:4px solid {GOLD};">
          <div style="font-size:0.72rem; font-weight:700; color:{TEXT_LITE}; text-transform:uppercase; letter-spacing:1px; margin-bottom:6px;">ID Agent Note</div>
          <div style="font-size:0.84rem; color:{TEXT_MID}; line-height:1.6;">{b['notes']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    if generate or "id_done" in st.session_state:
        st.session_state.id_done = True
        sec_header("📄", f"Generated Storyboard — {brief_key}")

        bar = st.progress(0, text="Instructional Designer Agent is working…")
        for i in range(100):
            time.sleep(0.004)
            bar.progress(i + 1, text=f"Generating storyboard… {i+1}%")
        bar.empty()

        for mod in b["modules"]:
            st.markdown(f"""
            <div class="sb-card">
              <div style="display:flex; align-items:center; gap:12px; margin-bottom:10px;">
                <div class="sb-seq" style="background:{mod['color']};">{mod['seq']}</div>
                <div style="flex:1;">
                  <div class="sb-title">{mod['title']}</div>
                  <div class="sb-type">{mod['type']}</div>
                </div>
                <span class="pill pill-slate">{mod.get('duration', '')}</span>
              </div>
              <div class="sb-narration">{mod['narration']}</div>
              <div class="sb-assets">📎 &nbsp;Assets: {mod['assets']}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        sec_header("✅", "QA Pre-Check — Before Handoff to Media Team")

        passed = sum(1 for _, _, p in QA_ITEMS if p)
        failed = len(QA_ITEMS) - passed

        qa_cols = st.columns([1, 3])
        with qa_cols[0]:
            st.markdown(f"""
            <div class="profile-card" style="text-align:center; padding:20px;">
              <div style="font-size:2.2rem; font-weight:900; color:{GREEN};">{passed}</div>
              <div style="font-size:0.75rem; color:{TEXT_LITE}; font-weight:600;">PASSED</div>
              <div style="height:1px; background:#EEF0F4; margin:10px 0;"></div>
              <div style="font-size:2.2rem; font-weight:900; color:{RED};">{failed}</div>
              <div style="font-size:0.75rem; color:{TEXT_LITE}; font-weight:600;">NEED ATTENTION</div>
              <div style="margin-top:12px; font-size:0.75rem; color:{TEXT_LITE}; line-height:1.5;">Human review required before authoring sign-off</div>
            </div>
            """, unsafe_allow_html=True)

        with qa_cols[1]:
            cats = {}
            for cat, item, ok in QA_ITEMS:
                cats.setdefault(cat, []).append((item, ok))

            c1, c2 = st.columns(2)
            for i, (cat, items) in enumerate(cats.items()):
                with (c1 if i % 2 == 0 else c2):
                    st.markdown(f'<div style="font-size:0.72rem; font-weight:700; color:{TEXT_LITE}; text-transform:uppercase; letter-spacing:1px; margin-bottom:4px;">{cat}</div>', unsafe_allow_html=True)
                    for item, ok in items:
                        icon_cls = "qa-pass" if ok else "qa-fail"
                        icon = "✓" if ok else "✗"
                        st.markdown(f'<div class="qa-item"><span class="{icon_cls}">{icon}</span>{item}</div>', unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)

        st.success("✅ Storyboard generated and logged to SharePoint with model version, timestamp, and prompt ID. Awaiting content team review before authoring begins.")


# ══════════════════════════════════════════════════════
# AGENT 3 — LEARNING CAMPAIGNER
# ══════════════════════════════════════════════════════
elif "📣" in agent:
    topbar("Learning Campaigner Agent", "UC-3 · Quick Win · Phase 1 · Always-on engagement")

    cl, cr = st.columns([1.1, 2.5])

    with cl:
        sec_header("📅", "Campaigns")
        if "sel_camp" not in st.session_state:
            st.session_state.sel_camp = CAMPAIGNS[0]["name"]

        for camp in CAMPAIGNS:
            sc = {
                "Active": GREEN, "Completed": NAVY, "Draft": "#D97706"
            }[camp["status"]]
            is_sel = st.session_state.sel_camp == camp["name"]
            if st.button(
                f"{camp['icon']}  {camp['name']}",
                key=f"cb_{camp['name']}",
                use_container_width=True,
            ):
                st.session_state.sel_camp = camp["name"]
                st.rerun()

        st.markdown("---")
        sec_header("➕", "New Campaign")
        st.text_input("Campaign name", placeholder="e.g. Safety Week Sprint", key="nc_name")
        st.selectbox("Trigger", ["Date-based", "Birthday/Anniversary", "Low engagement", "Manager-initiated"], key="nc_trigger")
        st.selectbox("Audience", ["All employees", "Department", "At-risk learners", "Specific role"], key="nc_aud")
        if st.button("Create Campaign", use_container_width=True):
            name = st.session_state.get("nc_name", "New Campaign")
            st.success(f"'{name}' created as Draft.")

    with cr:
        camp = next(c for c in CAMPAIGNS if c["name"] == st.session_state.sel_camp)
        sc = {"Active": GREEN, "Completed": NAVY, "Draft": "#D97706"}[camp["status"]]

        st.markdown(f"""
        <div class="camp-card" style="border-top-color:{camp['color']};">
          <div style="display:flex; align-items:center; gap:10px; margin-bottom:6px;">
            <div style="font-size:1.4rem;">{camp['icon']}</div>
            <div>
              <div class="camp-title">{camp['name']}</div>
              <div class="camp-meta">🔁 {camp['trigger']} &nbsp;·&nbsp; 👥 {camp['reach']} &nbsp;·&nbsp; 💬 {camp['channel']}</div>
            </div>
            <span class="pill" style="margin-left:auto; background:{sc}18; color:{sc};">{camp['status']}</span>
          </div>
          <div class="nudge-box">
            <div style="font-size:0.7rem; color:{TEXT_LITE}; font-style:normal; font-weight:700; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:6px;">Sample Personalised Nudge</div>
            {camp['nudge']}
          </div>
        </div>
        """, unsafe_allow_html=True)

        if camp["status"] != "Draft":
            sec_header("📈", "Campaign Performance")
            pm1, pm2, pm3 = st.columns(3)
            for col, val, lbl, tgt, c in [
                (pm1, f"{camp['sent']:,}",        "Nudges Sent",       "",       NAVY),
                (pm2, f"{camp['open_rate']}%",    "Open Rate",         "Target ≥50%", GREEN if camp['open_rate'] >= 50 else RED),
                (pm3, f"{camp['start_rate']}%",   "Learning Start Rate","Target ≥30%", GREEN if camp['start_rate'] >= 30 else RED),
            ]:
                col.markdown(f"""
                <div class="metric" style="border-top:3px solid {c};">
                  <div class="metric-val" style="color:{c};">{val}</div>
                  <div class="metric-lbl">{lbl}</div>
                  <div style="font-size:0.72rem; color:{TEXT_LITE}; margin-top:2px;">{tgt}</div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

        nb1, nb2 = st.columns(2)
        tone = nb1.select_slider("Tone", ["Formal", "Professional", "Friendly", "Celebratory"])
        length = nb2.radio("Length", ["Short", "Medium", "Full"], horizontal=True)

        if st.button("🔄  Regenerate Nudge", use_container_width=True):
            variants = {
                "Short":  f"{camp['icon']} Quick nudge: 15 minutes of learning awaits you today, {camp['name'].split()[0]}.",
                "Medium": camp['nudge'],
                "Full":   camp['nudge'] + "\n\n[Start now →] It only takes 15 minutes — the best investment you'll make today.",
            }
            st.markdown(f"""
            <div style="background:{GREEN_SOFT}; border:1.5px dashed {GREEN}; border-radius:12px; padding:16px 20px; margin-top:10px;">
              <div style="font-size:0.7rem; font-weight:700; color:{GREEN}; text-transform:uppercase; letter-spacing:1px; margin-bottom:8px;">Regenerated · {tone} · {length}</div>
              <div style="font-size:0.88rem; color:{TEXT_DARK}; line-height:1.7;">{variants[length]}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        sec_header("🎂", "Birthday Nudge Queue — Today")

        for name, initials, dept, course, status, sent in BDAY_QUEUE:
            sc2 = GREEN if sent else "#D97706"
            st.markdown(f"""
            <div class="bday-row">
              <div class="bday-avatar">{initials}</div>
              <div style="flex:1; min-width:0;">
                <div class="bday-name">{name} 🎂 &nbsp;<span style="font-weight:400; color:{TEXT_LITE}; font-size:0.78rem;">{dept}</span></div>
                <div class="bday-course">→ {course}</div>
              </div>
              <span class="pill" style="background:{sc2}18; color:{sc2}; font-size:0.72rem; white-space:nowrap;">{status}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f'<div class="info-footer">Nudges sent via Power Automate · HR birthday sync at 7:00 AM daily · Opt-outs honoured · Learning history pulled from Moodle</div>', unsafe_allow_html=True)
