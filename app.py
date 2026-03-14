import streamlit as st
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
    calculate_ats_score
)
import time
import streamlit.components.v1 as components

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
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            full_html = f.read()
    except FileNotFoundError:
        full_html = "<h1>Loading...</h1>"

    # Define a safe marker for the Disney-style loading screen
    loading_marker = "<!-- LOADING START -->"
    end_marker = "<!-- LOADING END -->"
    start_idx = full_html.find(loading_marker)
    end_idx = full_html.find(end_marker)

    if start_idx != -1 and end_idx != -1 and start_idx < end_idx:
        loading_html = full_html[start_idx + len(loading_marker):end_idx].strip()
    else:
        # fallback if markers missing
        loading_html = "<h1>Loading...</h1>"

    components.html(loading_html, height=1000, scrolling=False)

    # Visual progress bar simulation
    progress_bar = st.progress(0)
    for i in range(100):
        time.sleep(0.01)  # Smooth, fast loading
        progress_bar.progress(i + 1)

    st.session_state.app_loaded = True
    st.rerun()

# --- NAVIGATION & STATE ---
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "score" not in st.session_state:
    st.session_state.score = 0
if "score_category" not in st.session_state:
    st.session_state.score_category = "N/A"

# --- ASSETS LOADING ---
def load_assets():
    try:
        with open("style.css", "r") as f:
            css = f.read()
    except FileNotFoundError:
        css = ""

    try:
        with open("index.html", "r", encoding="utf-8") as f:
            full_html = f.read()
    except FileNotFoundError:
        full_html = "<h1>Dashboard</h1>"

    # Safe markers to find the dashboard header
    h_start = "<!-- DASHBOARD HEADER START -->"
    h_end = "<!-- DASHBOARD HEADER END -->"

    start_idx = full_html.find(h_start)
    end_idx = full_html.find(h_end)

    if start_idx != -1 and end_idx != -1 and start_idx < end_idx:
        html = full_html[start_idx + len(h_start):end_idx].strip()
    else:
        html = "<h1>Dashboard Header Content</h1>"  # fallback

    # Inject dynamic session values into HTML placeholders
    score_val = st.session_state.score if st.session_state.score > 0 else "--"
    rating_num = round(st.session_state.score / 10, 1) if st.session_state.score > 0 else "--"

    html = html.replace("{{SCORE}}", str(score_val))
    html = html.replace("{{RATING_NUM}}", str(rating_num))
    html = html.replace("{{RATING_TEXT}}", str(st.session_state.score_category))

    return f"<style>{css}</style>{html}"

# Render the dynamic header at the top
header_combined = load_assets()
components.html(header_combined, height=350, scrolling=False)

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>🎯 Navigation</h2>", unsafe_allow_html=True)
    pages = ["Home", "Resume Analyzer", "Skill Optimizer", "ATS Optimizer"]
    st.session_state.page = st.radio("Go to", pages, index=pages.index(st.session_state.page))
    st.divider()
    st.info("🔥 **Engine Status**: Online")

# --- PAGE ROUTING ---
if st.session_state.page == "Home":
    st.markdown("<h1 class='hero-title'>Welcome to ProResume Intelligence</h1>", unsafe_allow_html=True)
    st.write("Upload your resume to receive a comprehensive competency score and ATS optimization.")
    if st.button("Start New Analysis →"):
        st.session_state.page = "Resume Analyzer"
        st.rerun()

elif st.session_state.page == "Resume Analyzer":
    st.subheader("Upload your Resume (PDF/DOCX)")
    uploaded_file = st.file_uploader("Drop file here", type=["pdf", "docx"])

    if uploaded_file:
        file_bytes = uploaded_file.read()
        file_type = uploaded_file.name.split(".")[-1]

        with st.spinner("🚀 Initializing Smart Engine..."):
            text = parse_resume(file_bytes, file_type)
            skills = extract_skills(text)
            st.session_state.score = calculate_score(text, skills)
            st.session_state.score_category = get_score_category(st.session_state.score)
            st.session_state.user_resume_text = text
            st.rerun()  # Refresh to update dashboard scores

elif st.session_state.page == "Skill Optimizer":
    st.header("Skill Gap Analysis")
    if st.session_state.score == 0:
        st.warning("Please upload a resume in the Analyzer section first.")
    else:
        st.write("Comparing your profile against industry standards...")
        # Add skill gap visualization logic here

elif st.session_state.page == "ATS Optimizer":
    st.header("Bullet Point Optimizer")
    if 'user_resume_text' not in st.session_state:
        st.warning("Upload a resume to analyze bullet points.")
    else:
        bullets = extract_bullet_points(st.session_state.user_resume_text)
        for b in bullets[:5]:
            st.markdown(f"<div class='card'>{b}</div>", unsafe_allow_html=True)
