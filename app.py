import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from resume_parser import parse_resume
from analyzer import (extract_skills, calculate_score, generate_suggestions, 
                      improve_bullet_point, DOMAINS_DB, get_score_category, 
                      generate_backlogs, extract_bullet_points, 
                      check_grammar_communication, calculate_ats_score)
from fpdf import FPDF
import re
import io
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
    
    # FIX: Use the actual marker to split the loading screen
    if "" in full_html:
        loading_html = full_html.split("")[0]
    else:
        loading_html = full_html
        
    components.html(loading_html, height=1000, scrolling=False)
    
    time.sleep(1) 
    progress_bar = st.progress(0)
    for i in range(100):
        time.sleep(0.01)
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
        
    # FIX: Use markers to extract the Dashboard Header
    h_start = ""
    h_end = ""
    
    header_start = full_html.find(h_start)
    header_end = full_html.find(h_end)
    
    if header_start != -1 and header_end != -1:
        # Extract HTML between the tags
        html = full_html[header_start + len(h_start):header_end].strip()
    else:
        html = ""
    
    # Inject Dynamic Values
    html = html.replace("{{SCORE}}", str(st.session_state.score))
    
    score_val = st.session_state.score
    if isinstance(score_val, (int, float)):
        rating_num = round(score_val / 10, 1)
    else:
        rating_num = "--"
        
    rating_text = st.session_state.get('score_category', "--")
    html = html.replace("{{RATING_NUM}}", str(rating_num))
    html = html.replace("{{RATING_TEXT}}", str(rating_text))
    
    return f"<style>{css}</style>{html}"

header_combined = load_assets()

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>🎯 Navigation</h2>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135679.png", width=100)
    
    pages = ["Home", "Resume Analyzer", "Skill Optimizer", "ATS Optimizer"]
    page_index = pages.index(st.session_state.page) if st.session_state.page in pages else 0
    
    page = st.radio("Go to", pages, index=page_index, key="sidebar_radio")
    
    if page != st.session_state.page:
        st.session_state.page = page
        st.rerun()

# --- APP PAGES ---

def home_page():
    st.markdown("<h1 class='hero-title'>Optimized Professional Analysis</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='card'><h3>🚀 Strategy</h3><ul><li>Instant Score</li><li>Skill Gap Analysis</li></ul></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='card'><h3>🔥 Intelligence</h3><ul><li>ATS Optimization</li><li>Bullet Point Rewrite</li></ul></div>", unsafe_allow_html=True)
    
    if st.button("Start Analysis Now"):
        st.session_state.page = "Resume Analyzer"
        st.rerun()

def analyzer_page():
    st.markdown("<h2 class='hero-title'>Deep Resume Analysis</h2>", unsafe_allow_html=True)
    target_role = st.selectbox("🎯 Target Role", ["General"] + sorted(list(DOMAINS_DB.keys())))
    uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])
    
    if uploaded_file:
        file_bytes = uploaded_file.read()
        file_type = uploaded_file.name.split(".")[-1]
        
        with st.spinner("🚀 Analyzing..."):
            text = parse_resume(file_bytes, file_type)
            skills = extract_skills(text)
            score = calculate_score(text, skills)
            
            # Save to state and refresh header
            st.session_state.user_resume_text = text
            st.session_state.score = score
            st.session_state.skill_count = len(skills)
            st.session_state.user_skills_list = skills
            st.session_state.score_category = get_score_category(score)
            st.session_state.suggestions = generate_suggestions(text, skills)
            st.rerun()

def skill_optimizer_page():
    st.markdown("<h2 class='hero-title'>Skill Gap Analysis</h2>", unsafe_allow_html=True)
    if 'user_skills_list' not in st.session_state:
        st.warning("Please upload a resume first.")
        return
    st.info("Analyzing missing skills for your target industry...")

def ats_rewrite_page():
    st.markdown("<h2 class='hero-title'>ATS Optimizer</h2>", unsafe_allow_html=True)
    if 'user_resume_text' not in st.session_state:
        st.warning("Please upload a resume first.")
        return
    bullets = extract_bullet_points(st.session_state.user_resume_text)
    for b in bullets[:5]:
        st.markdown(f"<div class='card'>{b}</div>", unsafe_allow_html=True)

# --- MAIN RENDER ---
components.html(header_combined, height=480, scrolling=False)

if st.session_state.page == "Home": home_page()
elif st.session_state.page == "Resume Analyzer": analyzer_page()
elif st.session_state.page == "Skill Optimizer": skill_optimizer_page()
elif st.session_state.page == "ATS Optimizer": ats_rewrite_page()
