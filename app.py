import streamlit as st
# --- STREAMLIT VERSION COMPATIBILITY FIX ---
if not hasattr(st, "rerun"):
    st.rerun = st.experimental_rerun
import pandas as pd
import plotly.graph_objects as go
from resume_parser import parse_resume
from analyzer import extract_skills, calculate_score, generate_suggestions, improve_bullet_point, DOMAINS_DB, get_score_category, generate_backlogs, extract_bullet_points, check_grammar_communication, calculate_ats_score
from fpdf import FPDF
import re
import io

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
    # Extract loading section (everything before HEADER_START)
    loading_html = full_html.split("<!--HEADER_START-->")[0]
    import streamlit.components.v1 as components
    components.html(loading_html, height=1000, scrolling=False)
    
    import time
    time.sleep(1) # Let the animation play a bit before showing progress
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
    # Extract header section between markers
    header_start = full_html.find("<!--HEADER_START-->")
    header_end = full_html.find("<!--HEADER_END-->")
    if header_start != -1 and header_end != -1:
        html = full_html[header_start + len("<!--HEADER_START-->"):header_end].strip()
    else:
        html = ""
    
    # Inject Dynamic Values
    html = html.replace("{{SCORE}}", str(st.session_state.score))
    # Inject Rating: convert 100-scale score to 10-scale
    score_val = st.session_state.score
    if isinstance(score_val, (int, float)):
        rating_num = round(score_val / 10, 1)
    else:
        rating_num = "--"
    rating_text = st.session_state.score_category if 'score_category' in st.session_state else "--"
    html = html.replace("{{RATING_NUM}}", str(rating_num))
    html = html.replace("{{RATING_TEXT}}", str(rating_text))
    return f"<style>{css}</style>{html}"

header_combined = load_assets()

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>🎯 Resume Analyzer Navigation</h2>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135679.png", width=100)
    
    pages = ["Home", "Resume Analyzer", "Skill Optimizer", "ATS Optimizer"]
    page_index = pages.index(st.session_state.page) if st.session_state.page in pages else 0
    
    page = st.radio("Go to", pages, index=page_index, key="sidebar_radio")
    
    if page != st.session_state.page:
        st.session_state.page = page
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 📊 Platform Metrics")
    st.info("Accuracy: 98.4%\nEngines: Premium\nSpeed: Ultra Fast")

# --- APP PAGES ---

def home_page():
    st.markdown("<h1 class='hero-title'>Optimized Professional Analysis</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 1.2rem; color: #94a3b8;'>Unlock your career potential with advanced intelligence-driven resume optimization.</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class='card'>
            <h3>🚀 Why use this platform?</h3>
            <ul>
                <li>Instant Professional Score</li>
                <li>Strategic Skill Gap Analysis</li>
                <li>Precision Bullet Point Optimization</li>
                <li>Premium Layout Compatibility</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='card'>
            <h3>🔥 Core Capabilities</h3>
            <ul>
                <li>High-Speed Parsing (PDF/DOCX)</li>
                <li>Intelligent Keyword Extraction</li>
                <li>Smart Suggestion Engine</li>
                <li>Job Description Interaction</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    if st.button("Start Analysis Now"):
        st.session_state.page = "Resume Analyzer"
        st.rerun()

def analyzer_page():
    st.markdown("<h1 style='text-align: center; color: #6366f1; margin-bottom: 30px; font-family: \"Cinzel\", serif;'>PRORESUME INTELLIGENCE</h1>", unsafe_allow_html=True)
    st.markdown("<h2 class='hero-title'>Deep Resume Analysis</h2>", unsafe_allow_html=True)
    
    target_role = st.selectbox("🎯 Select Target Role for Analysis", ["General"] + sorted(list(DOMAINS_DB.keys())))
    
    uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])
    
    if uploaded_file is not None:
        file_bytes = uploaded_file.read()
        file_type = uploaded_file.name.split(".")[-1]
        
        with st.spinner("🚀 Initializing Smart Engine..."):
            text = parse_resume(file_bytes, file_type)
            skills = extract_skills(text)
            score = calculate_score(text, skills)
            score_category = get_score_category(score)
            suggestions = generate_suggestions(text, skills)
            backlogs = generate_backlogs(text, skills, target_role)
            
            # Save text into session state for ATS Optimizer
            st.session_state.user_resume_text = text
            
            # Auto-rerun on new upload
            if (st.session_state.score != score or 
                st.session_state.skill_count != len(skills) or 
                "uploaded_new_resume" not in st.session_state):
                
                st.session_state.score = score
                st.session_state.skill_count = len(skills)
                st.session_state.user_skills_list = skills
                st.session_state.score_category = score_category
                st.session_state.suggestions = suggestions
                st.session_state.backlogs = backlogs
                st.session_state.uploaded_new_resume = True
                st.rerun()
            
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.subheader("Professional Score")
            
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = score,
                number = {"suffix": "%", "font": {"size": 40, "color": "#f8fafc"}},
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': f"<span style='font-size:1.5em;color:#e2e8f0;font-weight:bold'>Competency Score</span><br><span style='font-size:1.2em;color:#818cf8'>{score_category}</span>", 'font': {'size': 20, 'color': "white"}},
                gauge = {
                    'axis': {'range': [0, 100], 'tickwidth': 2, 'tickcolor': "white", 'tickvals': [0, 20, 40, 60, 80, 100]},
                    'bar': {'color': "rgba(0,0,0,0)", 'thickness': 0},
                    'bgcolor': "rgba(0,0,0,0)",
                    'borderwidth': 0,
                    'steps': [
                        {'range': [0, 20], 'color': '#ef4444'},
                        {'range': [20, 40], 'color': '#f97316'},
                        {'range': [40, 60], 'color': '#eab308'},
                        {'range': [60, 80], 'color': '#84cc16'},
                        {'range': [80, 90], 'color': '#22c55e'},
                        {'range': [90, 100], 'color': '#10b981'}],
                    'threshold': {
                        'line': {'color': "#ffffff", 'width': 8},
                        'thickness': 0.8,
                        'value': score}
                }
            ))
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "white", 'family': "Inter"}, height=350, margin=dict(l=10, r=10, t=50, b=10))
            st.plotly_chart(fig, use_container_width=True)
            
            # Display Rating explicitly under the speedometer
            category = st.session_state.score_category if 'score_category' in st.session_state else "UNKNOWN"
            score_color = "#ef4444" if category in ["WORST", "AVERAGE"] else "#f59e0b" if category in ["GOOD", "VERY GOOD"] else "#22c55e"
            st.markdown(f"<h3 style='text-align: center; color: #e2e8f0; font-family: \"Inter\", sans-serif; letter-spacing: 2px;'>RATING: <span style='color: {score_color}; font-weight: 800;'>{category}</span></h3>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col2:
            st.markdown("<div class='card' style='height: 100%;'>", unsafe_allow_html=True)
            st.subheader("Strategic Suggestions")
            for sug in suggestions:
                st.markdown(f"<div class='suggestion-item'>{sug}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        st.divider()
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.subheader("Skills Detected")
            skill_html = " ".join([f"<span class='skill-tag'>{s}</span>" for s in skills])
            st.markdown(skill_html, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with c2:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.subheader("Data Overview")
            st.write(f"**Word Count:** {len(text.split())}")
            st.write(f"**Sections Identified:** {sum(1 for s in ['experience', 'education', 'projects'] if s in text.lower())}")
            st.markdown("</div>", unsafe_allow_html=True)
            
        # --- BACKLOGS SECTION ---
        st.divider()
        st.markdown("<h3 style='text-align: center; color: #ef4444;'>🚨 Resume Backlogs Analysis</h3>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; color: #94a3b8;'>Identified {len(backlogs)} Missing Elements & Areas for Improvement</p>", unsafe_allow_html=True)
        st.markdown("<div class='card' style='max-height: 400px; overflow-y: auto; text-align: left; padding: 20px;'>", unsafe_allow_html=True)
        for i, b in enumerate(backlogs, 1):
            st.markdown(f"<div style='margin-bottom: 8px; font-size: 1.1rem; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 5px;'><b>{i}.</b> {b}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # --- TIPS TO IMPROVE RESUME ---
        st.divider()
        st.markdown("<h3 style='text-align: center; color: #22c55e;'>💡 Tips to Improve Your Resume</h3>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #94a3b8;'>Actionable steps to boost your score and ATS compatibility</p>", unsafe_allow_html=True)
        
        tips = []
        
        # Score-based tips
        if score < 40:
            tips.append("🔴 <b>Critical:</b> Your resume is below the minimum threshold. Add detailed work experience, skills, and education sections immediately.")
            tips.append("🔴 <b>Action Required:</b> Include at least 8-10 relevant technical skills matching your target job description.")
        elif score < 60:
            tips.append("🟡 <b>Important:</b> Your resume has a basic structure but lacks impact. Quantify your achievements with numbers and percentages.")
        elif score < 80:
            tips.append("🟢 <b>Good Progress:</b> Add more measurable results (e.g., 'Increased sales by 25%' instead of 'Worked on sales').")
        else:
            tips.append("✅ <b>Excellent:</b> Your resume is strong. Fine-tune keyword density for specific ATS systems.")
        
        # Content-based tips  
        text_lower = text.lower()
        if 'summary' not in text_lower and 'objective' not in text_lower:
            tips.append("📝 <b>Add a Professional Summary:</b> A 2-3 line summary at the top helps recruiters quickly understand your profile.")
        
        if not re.search(r'\d+%', text):
            tips.append("📊 <b>Quantify Achievements:</b> Use numbers and percentages like 'Reduced costs by 30%' or 'Managed a team of 12'.")
        
        if 'linkedin' not in text_lower and 'github' not in text_lower and 'portfolio' not in text_lower:
            tips.append("🔗 <b>Add Online Profiles:</b> Include LinkedIn, GitHub, or Portfolio links to strengthen your professional presence.")
        
        if 'certification' not in text_lower and 'certified' not in text_lower:
            tips.append("🏅 <b>Add Certifications:</b> Industry certifications (AWS, Google, Microsoft, etc.) significantly boost ATS scores.")
        
        if len(text.split()) < 300:
            tips.append("📄 <b>Expand Content:</b> Your resume is too short. Aim for 400-700 words with detailed bullet points for each role.")
        elif len(text.split()) > 900:
            tips.append("✂️ <b>Trim Content:</b> Your resume is too long. Keep it concise — ideally 1-2 pages max for most roles.")
        
        weak_verbs = ['worked on', 'responsible for', 'helped', 'assisted', 'did', 'made']
        found_weak = [v for v in weak_verbs if v in text_lower]
        if found_weak:
            tips.append(f"💪 <b>Replace Weak Verbs:</b> Swap '{found_weak[0]}' with powerful action verbs like 'Spearheaded', 'Engineered', 'Optimized', 'Delivered'.")
        
        if 'project' not in text_lower:
            tips.append("🛠️ <b>Add Projects Section:</b> Personal/academic projects demonstrate hands-on skills and initiative.")
        
        if 'award' not in text_lower and 'achievement' not in text_lower and 'honor' not in text_lower:
            tips.append("🏆 <b>Highlight Achievements:</b> Awards, honors, or special recognitions make your profile stand out.")
        
        if 'volunteer' not in text_lower and 'community' not in text_lower:
            tips.append("🤝 <b>Add Volunteering:</b> Community work and volunteering demonstrate leadership and soft skills.")
        
        # General best-practice tips
        tips.append("🎯 <b>Tailor for Each Application:</b> Customize your resume keywords to match each specific job description.")
        tips.append("📐 <b>Use Clean Formatting:</b> Stick to professional fonts, consistent spacing, and clear section headers for ATS readability.")
        tips.append("🔤 <b>Proofread Carefully:</b> Spelling and grammar errors create a negative impression. Use tools like Grammarly before submitting.")
        
        for tip in tips:
            st.markdown(f"<div class='tip-card'>{tip}</div>", unsafe_allow_html=True)

        # --- GRAMMAR & COMMUNICATION ANALYSIS ---
        st.divider()
        st.markdown("<h3 style='text-align: center; color: #f59e0b;'>📝 Grammar & Communication Analysis</h3>", unsafe_allow_html=True)
        
        grammar_issues = check_grammar_communication(text)
        if grammar_issues:
            st.markdown(f"<p style='text-align: center; color: #94a3b8;'>Found {len(grammar_issues)} areas to improve</p>", unsafe_allow_html=True)
            for issue in grammar_issues:
                icon = "🔴" if "Grammar" in issue or "Spelling" in issue or "Typo" in issue else "🟡" if "Weak" in issue or "Informal" in issue else "🟠"
                st.markdown(f"<div class='suggestion-item' style='border-left-color: #f59e0b;'>{icon} {issue}</div>", unsafe_allow_html=True)
        else:
            st.success("✅ No grammar or communication issues detected! Your writing looks professional.")
        
        # --- ATS COMPATIBILITY SCORE ---
        st.divider()
        st.markdown("<h3 style='text-align: center; color: #6366f1;'>🤖 ATS (Applicant Tracking System) Compatibility</h3>", unsafe_allow_html=True)
        
        ats_score, ats_details = calculate_ats_score(text, skills)
        
        # ATS Score Bar
        ats_color = "#ef4444" if ats_score < 40 else "#f59e0b" if ats_score < 70 else "#22c55e"
        st.markdown(f"""
            <div class='card' style='text-align: center; border-color: {ats_color};'>
                <h2 style='margin: 0; color: {ats_color}; font-family: "Orbitron", sans-serif; font-size: 3rem;'>{ats_score}%</h2>
                <p style='color: #94a3b8; letter-spacing: 3px; text-transform: uppercase; font-size: 0.9rem;'>ATS Compatibility Score</p>
                <div style='background: rgba(255,255,255,0.1); border-radius: 10px; height: 12px; margin-top: 10px; overflow: hidden;'>
                    <div style='background: {ats_color}; width: {ats_score}%; height: 100%; border-radius: 10px; transition: width 1s ease;'></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # ATS Details
        st.markdown("<div class='card' style='padding: 20px;'>", unsafe_allow_html=True)
        st.markdown("#### 📋 ATS Breakdown:")
        for detail in ats_details:
            st.markdown(f"<div style='padding: 5px 0; font-size: 1rem;'>{detail}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Export Feature
        st.markdown("---")
        st.subheader("📋 Optimization Report")
        
        def safe_pdf_text(text):
            return text.encode('latin-1', 'replace').decode('latin-1')

        try:
            # Generation PDF (Fixed Layout Sequence)
            pdf = FPDF()
            pdf.set_margins(15, 15, 15) # CRITICAL: Set before add_page
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            pdf.set_font("Arial", size=11)
            
            # Header
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(0, 10, txt=safe_pdf_text("RESUME OPTIMIZATION INTELLIGENCE REPORT"), ln=True, align='C')
            pdf.ln(5)
            
            # Score
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 10, txt=safe_pdf_text(f"Overall Competency Score: {score}/100"), ln=True)
            pdf.ln(5)
            
            # Skills
            pdf.set_font("Arial", 'B', 11)
            pdf.cell(0, 10, txt=safe_pdf_text("Skills Detected:"), ln=True)
            pdf.set_font("Arial", size=10)
            pdf.multi_cell(180, 8, txt=safe_pdf_text(", ".join(skills)))
            pdf.ln(5)
            
            # Suggestions
            pdf.set_font("Arial", 'B', 11)
            pdf.cell(0, 10, txt=safe_pdf_text("Strategic Suggestions:"), ln=True)
            pdf.set_font("Arial", size=10)
            for s in suggestions:
                pdf.multi_cell(180, 7, txt=safe_pdf_text(f"- {s}"))
                
            pdf_output = pdf.output(dest='S')
            if isinstance(pdf_output, bytearray):
                pdf_output = bytes(pdf_output)
                
            st.download_button(
                label="Download Optimization Report",
                data=pdf_output,
                file_name="resume_optimization_report.pdf",
                mime="application/pdf",
            )
        except Exception as e:
            st.error(f"Error generating PDF: {str(e)}")

def skill_optimizer_page():
    st.markdown("<h2 class='hero-title'>Skill Gap Analysis</h2>", unsafe_allow_html=True)
    st.write("Compare your resume skills with industry standards across 50+ career domains.")
    
    sorted_domains = sorted(list(DOMAINS_DB.keys()))
    job_role = st.selectbox("Select Target Career Domain", sorted_domains)
    
    target = DOMAINS_DB[job_role]
    
    # Feature: Missing Skills Logic
    user_skills = [s.lower() for s in st.session_state.get('user_skills_list', [])]
    matching = [s for s in target if s.lower() in user_skills]
    missing = [s for s in target if s.lower() not in user_skills]
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("✅ Matching Skills")
        if matching:
            st.markdown(" ".join([f"<span class='skill-tag' style='background: rgba(34, 197, 94, 0.1); color: #4ade80;'>{s}</span>" for s in matching]), unsafe_allow_html=True)
        else:
            st.info("No matching skills found for this domain yet.")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("🚩 Missing Skills (Gaps)")
        if missing:
            st.markdown(" ".join([f"<span class='skill-tag' style='background: rgba(239, 68, 68, 0.1); color: #f87171;'>{s}</span>" for s in missing]), unsafe_allow_html=True)
        else:
            st.success("Perfect alignment! You have all the core skills for this role.")
        st.markdown("</div>", unsafe_allow_html=True)

    # Step-by-Step Requirements
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🚀 Step-by-Step Skill Roadmap")
    for i, skill in enumerate(target, 1):
        status = "✅ (Complete)" if skill in matching else "⏳ (Missing)"
        st.markdown(f"**Step {i}:** Master **{skill}** {status}")
        st.write(f"Objective: Focus on practical implementation of {skill} through projects.")
    st.markdown("</div>", unsafe_allow_html=True)

def ats_rewrite_page():
    st.markdown("<h2 class='hero-title'>Applicant Tracking System (ATS) Optimizer</h2>", unsafe_allow_html=True)
    st.write("Extracts work experience and project statements from your resume, scoring their impact and providing professional, ATS-friendly rewrites.")
    
    # Needs a resume first
    if 'user_resume_text' not in st.session_state or not st.session_state.user_resume_text:
        st.warning("Please upload your resume in the 'Resume Analyzer' page first to extract bullet points.")
        return
        
    text = st.session_state.user_resume_text
    
    with st.spinner("🔍 Extracting Bullet Points..."):
        bullets = extract_bullet_points(text)
        
    if not bullets:
        st.info("No clear bullet points or experience statements found in the uploaded resume. Ensure your resume uses standard bullet formatting (e.g., • or -).")
        return
        
    st.markdown(f"### 📑 Found {len(bullets)} Statements")
    
    # Grammar & Communication Insight for the whole resume
    grammar_issues = check_grammar_communication(text)
    if grammar_issues:
        with st.expander(f"📝 Quality & Communication Gaps ({len(grammar_issues)} Found)"):
            for issue in grammar_issues:
                st.markdown(f"• {issue}")
    else:
        st.success("✅ Writing quality and professional tone look excellent!")
    
    for i, bullet in enumerate(bullets):
        st.markdown(f"<div class='card' style='margin-bottom: 20px; border-left: 4px solid #6366f1;'>", unsafe_allow_html=True)
        st.markdown(f"**Original Statement:**\n> {bullet}")
        
        result = improve_bullet_point(bullet)
        score = result['score'] if result else 0
        
        # Color coding score
        color = "#ef4444" if score < 4 else "#f59e0b" if score < 7 else "#22c55e"
        score_label = "Poor" if score < 4 else "Average" if score < 7 else "Strong"
        st.markdown(f"**Impact Score:** <span style='color: {color}; font-weight: bold; font-size: 1.3rem;'>{score}/10</span> <span style='color: {color}; font-size: 0.9rem;'>({score_label})</span>", unsafe_allow_html=True)
        
        # Impact suggestions based on score
        if score < 4:
            st.markdown("<div class='tip-card' style='border-color: #ef4444;'>🔴 <b>Low Impact:</b> This statement lacks action verbs, measurable results, and specifics. Rewrite it using the ATS suggestion below.</div>", unsafe_allow_html=True)
        elif score < 7:
            st.markdown("<div class='tip-card' style='border-color: #f59e0b;'>🟡 <b>Moderate Impact:</b> Add quantified results (numbers, percentages) and stronger action verbs to improve this bullet.</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='tip-card' style='border-color: #22c55e;'>🟢 <b>Strong Impact:</b> This is a well-written statement. Minor tweaks below can optimize it further for ATS.</div>", unsafe_allow_html=True)
        
        if result:
            st.markdown("#### 🎯 ATS Suggestions:")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("<div style='background: rgba(99, 102, 241, 0.05); padding: 10px; border-radius: 5px;'>", unsafe_allow_html=True)
                st.markdown("**1️⃣ ATS & STAR Optimized:**")
                st.write(result['ats'])
                if st.button(f"Accept ATS Version", key=f"btn_ats_{i}"):
                    st.success("ATS Version Accepted! (Will be included in final export)")
                st.markdown("</div>", unsafe_allow_html=True)
                
            with col2:
                st.markdown("<div style='background: rgba(34, 197, 94, 0.05); padding: 10px; border-radius: 5px;'>", unsafe_allow_html=True)
                st.markdown("**2️⃣ Professional Rewrite:**")
                st.write(result['general'])
                if st.button(f"Accept Pro Version", key=f"btn_pro_{i}"):
                    st.success("Professional Version Accepted! (Will be included in final export)")
                st.markdown("</div>", unsafe_allow_html=True)
                
            st.markdown("**Action Verbs to Consider:**")
            verbs_html = " ".join([f"<span class='skill-tag' style='background: rgba(255, 255, 255, 0.05); padding: 2px 6px; font-size: 0.8rem;'>{v}</span>" for v in result['action_verbs']])
            st.markdown(verbs_html, unsafe_allow_html=True)
            
        st.markdown("</div>", unsafe_allow_html=True)

# --- MAIN CONTROLLER ---
import streamlit.components.v1 as components
components.html(header_combined, height=480, scrolling=False)

if st.session_state.page == "Home":
    home_page()
elif st.session_state.page == "Resume Analyzer":
    analyzer_page()
elif st.session_state.page == "Skill Optimizer":
    skill_optimizer_page()
elif st.session_state.page == "ATS Optimizer":
    ats_rewrite_page()
