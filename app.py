import streamlit as st

# --- STREAMLIT RERUN COMPATIBILITY FIX ---
# Works for both old and new versions
if not hasattr(st, "rerun"):
    st.rerun = st.experimental_rerun

import pandas as pd
import plotly.graph_objects as go
from resume_parser import parse_resume
from analyzer import (
    extract_skills,
    calculate_score,
    generate_suggestions,
    improve_bullet_point,
    DOMAINS_DB,
    get_score_category,
    generate_backlogs,
    extract_bullet_points,
    check_grammar_communication,
    calculate_ats_score,
)
from fpdf import FPDF
import re
import io
import streamlit.components.v1 as components
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="ProResume Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- LOADING SEQUENCE ---
if "app_loaded" not in st.session_state:
    st.session_state.app_loaded = False

if not st.session_state.app_loaded:
    with open("index.html", "r", encoding="utf-8") as f:
        full_html = f.read()

    loading_html = full_html.split("<!--HEADER_START-->")[0]

    components.html(loading_html, height=1000, scrolling=False)

    time.sleep(1)

    progress_bar = st.progress(0)
    for i in range(100):
        time.sleep(0.02)
        progress_bar.progress(i + 1)

    st.session_state.app_loaded = True
    st.rerun()

# --- NAVIGATION STATE ---
if "page" not in st.session_state:
    st.session_state.page = "Home"

if "score" not in st.session_state:
    st.session_state.score = "--"

if "skill_count" not in st.session_state:
    st.session_state.skill_count = "--"


# --- ASSETS LOADING ---
def load_assets():
    with open("style.css", "r") as f:
        css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

    with open("script.js", "r") as f:
        st.markdown(f"<script>{f.read()}</script>", unsafe_allow_html=True)

    with open("index.html", "r", encoding="utf-8") as f:
        full_html = f.read()

    header_start = full_html.find("<!--HEADER_START-->")
    header_end = full_html.find("<!--HEADER_END-->")

    if header_start != -1 and header_end != -1:
        html = full_html[
            header_start + len("<!--HEADER_START-->") : header_end
        ].strip()
    else:
        html = ""

    html = html.replace("{{SCORE}}", str(st.session_state.score))

    score_val = st.session_state.score

    if isinstance(score_val, (int, float)):
        rating_num = round(score_val / 10, 1)
    else:
        rating_num = "--"

    rating_text = (
        st.session_state.score_category
        if "score_category" in st.session_state
        else "--"
    )

    html = html.replace("{{RATING_NUM}}", str(rating_num))
    html = html.replace("{{RATING_TEXT}}", str(rating_text))

    return f"<style>{css}</style>{html}"


header_combined = load_assets()

# --- SIDEBAR ---
with st.sidebar:

    st.markdown(
        "<h2 style='text-align: center;'>🎯 Resume Analyzer Navigation</h2>",
        unsafe_allow_html=True,
    )

    st.image(
        "https://cdn-icons-png.flaticon.com/512/3135/3135679.png",
        width=100,
    )

    pages = ["Home", "Resume Analyzer", "Skill Optimizer", "ATS Optimizer"]

    page_index = (
        pages.index(st.session_state.page)
        if st.session_state.page in pages
        else 0
    )

    page = st.radio("Go to", pages, index=page_index)

    if page != st.session_state.page:
        st.session_state.page = page
        st.rerun()

    st.markdown("---")

    st.markdown("### 📊 Platform Metrics")

    st.info(
        """
Accuracy: 98.4%
Engines: Premium
Speed: Ultra Fast
"""
    )

# --- HOME PAGE ---
def home_page():

    st.markdown(
        "<h1 class='hero-title'>Optimized Professional Analysis</h1>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<p style='font-size: 1.2rem; color: #94a3b8;'>Unlock your career potential with advanced intelligence-driven resume optimization.</p>",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            """
<div class='card'>
<h3>🚀 Why use this platform?</h3>
<ul>
<li>Instant Professional Score</li>
<li>Strategic Skill Gap Analysis</li>
<li>Precision Bullet Point Optimization</li>
<li>Premium Layout Compatibility</li>
</ul>
</div>
""",
            unsafe_allow_html=True,
        )

    with col2:

        st.markdown(
            """
<div class='card'>
<h3>🔥 Core Capabilities</h3>
<ul>
<li>High-Speed Parsing (PDF/DOCX)</li>
<li>Intelligent Keyword Extraction</li>
<li>Smart Suggestion Engine</li>
<li>Job Description Interaction</li>
</ul>
</div>
""",
            unsafe_allow_html=True,
        )

    st.divider()

    if st.button("Start Analysis Now"):
        st.session_state.page = "Resume Analyzer"
        st.rerun()


# --- RESUME ANALYZER PAGE ---
def analyzer_page():

    st.markdown(
        "<h1 style='text-align: center; color: #6366f1;'>PRORESUME INTELLIGENCE</h1>",
        unsafe_allow_html=True,
    )

    target_role = st.selectbox(
        "🎯 Select Target Role for Analysis",
        ["General"] + sorted(list(DOMAINS_DB.keys())),
    )

    uploaded_file = st.file_uploader(
        "Upload your resume (PDF or DOCX)",
        type=["pdf", "docx"],
    )

    if uploaded_file:

        file_bytes = uploaded_file.read()

        file_type = uploaded_file.name.split(".")[-1]

        with st.spinner("🚀 Initializing Smart Engine..."):

            text = parse_resume(file_bytes, file_type)

            skills = extract_skills(text)

            score = calculate_score(text, skills)

            score_category = get_score_category(score)

            suggestions = generate_suggestions(text, skills)

            backlogs = generate_backlogs(text, skills, target_role)

            st.session_state.user_resume_text = text

            if (
                st.session_state.score != score
                or st.session_state.skill_count != len(skills)
                or "uploaded_new_resume" not in st.session_state
            ):

                st.session_state.score = score
                st.session_state.skill_count = len(skills)
                st.session_state.user_skills_list = skills
                st.session_state.score_category = score_category
                st.session_state.suggestions = suggestions
                st.session_state.backlogs = backlogs
                st.session_state.uploaded_new_resume = True

                st.rerun()

        st.subheader("Professional Score")

        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=score,
                number={"suffix": "%"},
                title={"text": f"Competency Score<br>{score_category}"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "steps": [
                        {"range": [0, 20], "color": "#ef4444"},
                        {"range": [20, 40], "color": "#f97316"},
                        {"range": [40, 60], "color": "#eab308"},
                        {"range": [60, 80], "color": "#84cc16"},
                        {"range": [80, 100], "color": "#22c55e"},
                    ],
                },
            )
        )

        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Strategic Suggestions")

        for sug in suggestions:
            st.write("•", sug)


# --- SKILL OPTIMIZER ---
def skill_optimizer_page():

    st.markdown(
        "<h2 class='hero-title'>Skill Gap Analysis</h2>",
        unsafe_allow_html=True,
    )

    sorted_domains = sorted(list(DOMAINS_DB.keys()))

    job_role = st.selectbox("Select Target Career Domain", sorted_domains)

    target = DOMAINS_DB[job_role]

    user_skills = [
        s.lower()
        for s in st.session_state.get("user_skills_list", [])
    ]

    matching = [s for s in target if s.lower() in user_skills]

    missing = [s for s in target if s.lower() not in user_skills]

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Matching Skills")

        for s in matching:
            st.success(s)

    with col2:

        st.subheader("Missing Skills")

        for s in missing:
            st.error(s)


# --- ATS OPTIMIZER ---
def ats_rewrite_page():

    st.markdown(
        "<h2 class='hero-title'>ATS Optimizer</h2>",
        unsafe_allow_html=True,
    )

    if "user_resume_text" not in st.session_state:

        st.warning(
            "Upload resume in Resume Analyzer first."
        )

        return

    text = st.session_state.user_resume_text

    bullets = extract_bullet_points(text)

    st.write("Found", len(bullets), "bullet points")

    for bullet in bullets:

        st.markdown("**Original:**")

        st.write(bullet)

        result = improve_bullet_point(bullet)

        if result:

            st.markdown("**ATS Version:**")

            st.success(result["ats"])

            st.markdown("**Professional Version:**")

            st.info(result["general"])


# --- MAIN CONTROLLER ---

components.html(header_combined, height=480)

if st.session_state.page == "Home":
    home_page()

elif st.session_state.page == "Resume Analyzer":
    analyzer_page()

elif st.session_state.page == "Skill Optimizer":
    skill_optimizer_page()

elif st.session_state.page == "ATS Optimizer":
    ats_rewrite_page()
