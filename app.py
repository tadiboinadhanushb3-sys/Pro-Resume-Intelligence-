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
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            full_html = f.read()
        
        # Split logic: Extract everything BEFORE the header tag for the loader
        if "" in full_html:
            loading_html = full_html.split("")[0]
        else:
            loading_html = full_html # Fallback
            
        components.html(loading_html, height=1000, scrolling=False)
        
        time.sleep(1) 
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress_bar.progress(i + 1)
            
        st.session_state.app_loaded = True
        st.rerun()
    except FileNotFoundError:
        st.error("index.html not found. Please ensure the file exists.")
        st.stop()

# --- NAVIGATION & APP STATE ---
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "score" not in st.session_state:
    st.session_state.score = 0
if "skill_count" not in st.session_state:
    st.session_state.skill_count = 0
if "score_category" not in st.session_state:
    st.session_state.score_category = "N/A"

# --- ASSETS LOADING ---
def load_assets():
    try:
        with open("style.css", "r") as f:
            css = f.read()
        with open("index.html", "r", encoding="utf-8") as f:
            full_html = f.read()
            
        h_start = ""
        h_end = ""
        
        start_idx = full_html.find(h_start)
        end_idx = full_html.find(h_end)
        
        if start_idx != -1 and end_idx != -1:
            # Extract only the dashboard header part
            html = full_html[start_idx + len(h_start):end_idx].strip()
        else:
            html = "<div style='color:red;'>Error: Dashboard markers not found in index.html</div>"
        
        # Inject Dynamic Values into the HTML for the dashboard
        current_score = st.session_state.score if st.session_state.score > 0 else "--"
        html = html.replace("{{SCORE}}", str(current_score))
        
        rating_num = round(st.session_state.score / 10, 1) if st.session_state.score > 0 else "--"
        html = html.replace("{{RATING_NUM}}", str(rating_num))
        html = html.replace("{{RATING_TEXT}}", str(st.session_state.score_category))
        
        return f"<style>{css}</style>{html}"
    except Exception as e:
        return f"<style>body{{background:black; color:white;}}</style><div>Error loading assets: {e}</div>"

# Generate the header component
header_combined = load_assets()

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>🎯 Navigation</h2>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135679.png", width=100)
    
    pages = ["Home", "Resume Analyzer", "Skill Optimizer", "ATS Optimizer"]
    page_index = pages.index(st.session_state.page) if st.session_state.page in pages else 0
    
    selected_page = st.radio("Go to", pages, index=page_index, key="nav_radio")
    
    if selected_page != st.session_state.page:
        st.session_state.page = selected_page
        st.rerun()
    
    st.markdown("---")
    st.info("🔥 **Engine Status**: Online\n⚡ **Speed**: Ultra")

# --- PAGE DEFINITIONS ---

def home_page():
    st.markdown("<h1 class='hero-title'>Optimized Professional Analysis</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='card'><h3>🚀 Why use this?</h3><ul><li>Instant Score</li><li>Skill Gap Analysis</li><li>ATS Optimization</li></ul></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='card'><h3>🔥 Core Tech</h3><ul><li>Smart Parsing</li><li>Keyword Extraction</li><li>Suggestion Engine</li></ul></div>", unsafe_allow_html=True)
    
    if st.button("Get Started →"):
        st.session_state.page = "Resume Analyzer"
        st.rerun()

def analyzer_page():
    st.markdown("<h2 class='hero-title'>Deep Resume Analysis</h2>", unsafe_allow_html=True)
    
    target_role = st.selectbox("🎯 Target Domain", ["General"] + sorted(list(DOMAINS_DB.keys())))
    uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])
    
    if uploaded_file:
        with st.spinner("🚀 Analyzing your profile..."):
            file_bytes = uploaded_file.read()
            file_type = uploaded_file.name.split(".")[-1]
            
            text = parse_resume(file_bytes, file_type)
            skills = extract_skills(text)
            score = calculate_score(text, skills)
            
            # Update values and trigger a rerun to update the Header HTML
            st.session_state.user_resume_text = text
            st.session_state.score = score
            st.session_state.skill_count = len(skills)
            st.session_state.user_skills_list = skills
            st.session_state.score_category = get_score_category(score)
            st.session_state.suggestions = generate_suggestions(text, skills)
            st.session_state.backlogs = generate_backlogs(text, skills, target_role)
            st.rerun()

    if st.session_state.score > 0:
        c1, c2 = st.columns([1, 2])
        with c1:
            st.markdown(f"<div class='card' style='text-align:center;'><h2>{st.session_state.score}%</h2><p>{st.session_state.score_category}</p></div>", unsafe_allow_html=True)
        with c2:
            st.markdown("<div class='card'><h3>Suggestions</h3>", unsafe_allow_html=True)
            for s in st.session_state.get('suggestions', [])[:4]:
                st.write(f"• {s}")
            st.markdown("</div>", unsafe_allow_html=True)

def skill_optimizer_page():
    st.markdown("<h2 class='hero-title'>Skill Gap Analysis</h2>", unsafe_allow_html=True)
    if not st.session_state.get('user_skills_list'):
        st.warning("Please analyze a resume first.")
        return
        
    job_role = st.selectbox("Industry Role", sorted(list(DOMAINS_DB.keys())))
    target = DOMAINS_DB[job_role]
    user_skills = [s.lower() for s in st.session_state.user_skills_list]
    
    missing = [s for s in target if s.lower() not in user_skills]
    
    st.subheader("🚩 Missing Skills")
    if missing:
        st.markdown(" ".join([f"<span class='skill-tag' style='background:rgba(239,68,68,0.2);'>{s}</span>" for s in missing]), unsafe_allow_html=True)
    else:
        st.success("You are a perfect match!")

def ats_rewrite_page():
    st.markdown("<h2 class='hero-title'>ATS Optimizer</h2>", unsafe_allow_html=True)
    if not st.session_state.get('user_resume_text'):
        st.warning("Please upload a resume first.")
        return
    
    bullets = extract_bullet_points(st.session_state.user_resume_text)
    for i, b in enumerate(bullets[:5]):
        with st.expander(f"Bullet Point {i+1}"):
            res = improve_bullet_point(b)
            st.markdown(f"**Original:** {b}")
            st.success(f"**ATS Suggested:** {res['ats']}")

# --- MAIN RENDER ---
# Render the Dashboard Header
components.html(header_combined, height=480, scrolling=False)

# Display content based on navigation
if st.session_state.page == "Home": home_page()
elif st.session_state.page == "Resume Analyzer": analyzer_page()
elif st.session_state.page == "Skill Optimizer": skill_optimizer_page()
elif st.session_state.page == "ATS Optimizer": ats_rewrite_page()
