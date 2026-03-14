import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from resume_parser import parse_resume
from analyzer import (extract_skills, calculate_score, generate_suggestions, 
                      improve_bullet_point, DOMAINS_DB, get_score_category, 
                      generate_backlogs, extract_bullet_points, 
                      check_grammar_communication, calculate_ats_score)
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
    with open("index.html", "r", encoding="utf-8") as f:
        full_html = f.read()
    
    # We split by the START tag to get only the Disney Loading Screen part
    loading_html = full_html.split("")[0]
    
    components.html(loading_html, height=1000, scrolling=False)
    
    # Progress simulation
    progress_bar = st.progress(0)
    for i in range(100):
        time.sleep(0.02)
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
    with open("style.css", "r") as f:
        css = f.read()
    with open("index.html", "r", encoding="utf-8") as f:
        full_html = f.read()
        
    # Extract only the Dashboard Header section
    h_start = ""
    h_end = ""
    
    start_idx = full_html.find(h_start)
    end_idx = full_html.find(h_end)
    
    # Get the HTML between the two markers
    html = full_html[start_idx + len(h_start):end_idx].strip()
    
    # Dynamic Replacement for your <div> sections
    score_val = st.session_state.score if st.session_state.score > 0 else "--"
    rating_num = round(st.session_state.score / 10, 1) if st.session_state.score > 0 else "--"
    
    html = html.replace("{{SCORE}}", str(score_val))
    html = html.replace("{{RATING_NUM}}", str(rating_num))
    html = html.replace("{{RATING_TEXT}}", str(st.session_state.score_category))
    
    return f"<style>{css}</style>{html}"

# Render the dynamic header
header_combined = load_assets()
components.html(header_combined, height=350, scrolling=False)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>🎯 Navigation</h2>", unsafe_allow_html=True)
    pages = ["Home", "Resume Analyzer", "Skill Optimizer", "ATS Optimizer"]
    st.session_state.page = st.radio("Go to", pages, index=pages.index(st.session_state.page))

# --- PAGE ROUTING ---
if st.session_state.page == "Home":
    st.markdown("<h1 class='hero-title'>Welcome to ProResume</h1>", unsafe_allow_html=True)
    if st.button("Start New Analysis"):
        st.session_state.page = "Resume Analyzer"
        st.rerun()

elif st.session_state.page == "Resume Analyzer":
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
    if uploaded_file:
        with st.spinner("Analyzing..."):
            # Mocking the processing (replace with your actual function calls)
            text = parse_resume(uploaded_file.read(), "pdf")
            skills = extract_skills(text)
            st.session_state.score = calculate_score(text, skills)
            st.session_state.score_category = get_score_category(st.session_state.score)
            st.rerun() # Refresh to update the Header Score
