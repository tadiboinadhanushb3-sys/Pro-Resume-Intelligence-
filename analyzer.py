import re

# Analysis Engine (Lightweight & High-Speed)

SKILLS_DB = [
    "Python", "Java", "C++", "JavaScript", "React", "Angular", "Vue", "Node.js", 
    "Express", "Flask", "FastAPI", "Django", "SQL", "PostgreSQL", "MongoDB", 
    "Docker", "Kubernetes", "AWS", "Azure", "GCP", "Machine Learning", 
    "Data Science", "AI", "NLP", "Computer Vision", "Git", "HTML", "CSS", 
    "Tailwind", "Bootstrap", "TypeScript", "Redux", "GraphQL", "REST API",
    "Leadership", "Communication", "Problem Solving", "Teamwork", "Time Management", "Analytical Skills",
    "Project Management", "Agile", "Scrum", "Jira", "Trello", "Kanban", "Product Management",
    "SQL Server", "MySQL", "Redis", "Elasticsearch",
    "PyTorch", "TensorFlow", "Keras", "Scikit-Learn", "OpenCV", "Matplotlib", "Seaborn",
    "AWS Lambda", "AWS S3", "AWS EC2", "AWS RDS", "Google Cloud Platform", "Terraform", "Ansible", 
    "Jenkins", "CircleCI", "Bitbucket", "GitLab", "Figma", "Sketch", "Prototyping", "User Research",
    "Adobe Suite", "Photoshop", "Illustrator", "InDesign", "Web Design", "Graphic Design",
    "SEO", "SEM", "Content Strategy", "Digital Marketing", "Social Media Marketing", "Copywriting",
    "Salesforce", "SAP", "Excel", "Power BI", "Tableau", "Blockchain", "Solidity", "Rust", "Go",
    "C#", ".NET", "Quality Assurance", "Selenium", "Cypress", "Appium", "Mobile Development",
    "Swift", "Kotlin", "Objective-C", "Flutter", "React Native", "Unity", "Unreal Engine"
]

DOMAINS_DB = {
    "Software Engineer": ["Python", "Java", "Data Structures", "Algorithms", "Git", "SQL"],
    "Data Scientist": ["Python", "Machine Learning", "Statistics", "Pandas", "SQL", "R"],
    "Product Manager": ["Leadership", "Agile", "Roadmapping", "Market Analysis", "Communication"],
    "UI/UX Designer": ["Figma", "Prototyping", "User Research", "Adobe Suite", "Design Systems"],
    "Frontend Developer": ["HTML", "CSS", "JavaScript", "React", "TypeScript", "Tailwind"],
    "Backend Developer": ["Node.js", "Express", "Python", "Flask", "SQL", "REST API"],
    "Full Stack Developer": ["React", "Node.js", "JavaScript", "HTML", "CSS", "SQL"],
    "DevOps Engineer": ["Docker", "Kubernetes", "AWS", "Terraform", "Jenkins", "Ansible"],
    "Cloud Architect": ["AWS", "Azure", "GCP", "Cloud Security", "Infrastructure as Code"],
    "Data Engineer": ["SQL", "ETL", "Python", "Spark", "Hadoop", "Data Warehousing"],
    "Cybersecurity Analyst": ["Network Security", "Ethical Hacking", "Cryptography", "Linux", "SOC"],
    "Mobile App Developer": ["Swift", "Kotlin", "Flutter", "React Native", "Mobile Design"],
    "Embedded Systems Engineer": ["C", "C++", "Microcontrollers", "RTOS", "Embedded Linux"],
    "QA Automation Engineer": ["Selenium", "Java", "Python", "Jenkins", "Unit Testing"],
    "AI/ML Engineer": ["PyTorch", "TensorFlow", "NLP", "Computer Vision", "Deep Learning"],
    "Database Administrator": ["SQL Server", "MySQL", "PostgreSQL", "Query Optimization", "DBA"],
    "Network Engineer": ["Cisco", "TCP/IP", "VPN", "Routing & Switching", "Network Security"],
    "System Administrator": ["Linux", "Windows Server", "Active Directory", "Bash", "Shell Scripting"],
    "Blockchain Developer": ["Solidity", "Ethereum", "Blockchain Architecture", "Rust", "Go"],
    "Game Developer": ["Unity", "Unreal Engine", "C#", "C++", "Game Physics", "3D Modeling"],
    "Business Analyst": ["Requirements Gathering", "SQL", "Excel", "Data Visualization", "UML"],
    "Marketing Manager": ["SEO", "Digital Marketing", "Content Strategy", "Market Research"],
    "Sales Executive": ["CRM", "Lead Generation", "Negotiation", "Communication", "Cold Calling"],
    "Human Resources Manager": ["Talent Acquisition", "Employee Relations", "HRIS", "Compliance"],
    "Financial Analyst": ["Financial Modeling", "Excel", "Forecasting", "Valuation", "Accounting"],
    "Content Strategy Manager": ["Content Strategy", "SEO", "Copywriting", "CMS", "Editorial"],
    "Social Media Manager": ["Social Media Strategy", "Content Creation", "Analytics", "Engagement"],
    "SEO Specialist": ["Keyword Research", "On-page SEO", "Backlinking", "Google Analytics"],
    "E-commerce Manager": ["Shopify", "Magento", "Digital Sales", "Inventory Management"],
    "Supply Chain Manager": ["Logistics", "Procurement", "Inventory Control", "ERP Systems"],
    "Project Manager": ["Agile", "Scrum", "PMP", "Project Planning", "Stakeholder Management"],
    "Customer Success Manager": ["Relationship Management", "Customer Retention", "Onboarding"],
    "Operations Manager": ["Process Improvement", "Strategic Planning", "Efficiency", "Team Management"],
    "IT Support Specialist": ["Troubleshooting", "Desktop Support", "Help Desk", "Hardware Repair"],
    "Salesforce Developer": ["Apex", "SOQL", "Visualforce", "Salesforce Lightning", "CRM"],
    "SAP Consultant": ["SAP ERP", "ABAP", "SAP Modules", "Business Process Mapping"],
    "Technical Writer": ["Documentation", "API Documentation", "DITA", "Markdown", "Clear Writing"],
    "Digital Marketer": ["PPC", "SEM", "Email Marketing", "Google Ads", "Content Marketing"],
    "Data Architect": ["Data Modeling", "Big Data", "Enterprise Data Strategy", "ETL"],
    "Information Security Manager": ["Risk Management", "ISO 27001", "Compliance", "Security Audits"],
    "Solutions Architect": ["System Architecture", "Integration", "Technical Design", "Client Facing"],
    "Business Intelligence Developer": ["Power BI", "Tableau", "DAX", "SQL Server Analysis Services"],
    "Web Designer": ["Layout Design", "Color Theory", "Responsive Design", "UI Design"],
    "Graphic Designer": ["Photoshop", "Illustrator", "Branding", "Visual Identity", "Typography"],
    "Video Editor": ["Premiere Pro", "After Effects", "Color Grading", "Sound Editing"],
    "Copywriter": ["Persuasive Writing", "Brand Voice", "Ad Copy", "Content Creation"],
    "Product Designer": ["UX", "Industrial Design", "Prototyping", "User-Centered Design"],
    "Interaction Designer": ["HCI", "User Flows", "Wireframing", "Interactive Prototypes"],
    "Growth Hacker": ["A/B Testing", "Aquisition Strategy", "Funnel Optimization", "Data Driven"],
    "Risk Manager": ["Risk Assessment", "Financial Risk", "Compliance", "Internal Audit"]
}

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text

def extract_skills(text):
    text = text.lower()
    found_skills = []
    for skill in SKILLS_DB:
        if re.search(r'\b' + re.escape(skill.lower()) + r'\b', text):
            found_skills.append(skill)
    return list(set(found_skills))

def calculate_score(text, skills):
    score = 0
    # 1. Skill Score (Weight: 40%)
    skill_score = min(len(skills) * 5, 40)
    score += skill_score
    
    # 2. Length Score (Weight: 20%)
    word_count = len(text.split())
    if 300 <= word_count <= 800:
        score += 20
    elif word_count > 800:
        score += 15
    else:
        score += 10
        
    # 3. Formatting/Keywords Score (Weight: 40%)
    sections = ["experience", "education", "projects", "summary", "contact"]
    section_score = 0
    for section in sections:
        if section in text.lower():
            section_score += 8
    score += section_score
    
    return min(score, 100)

def generate_suggestions(text, skills):
    suggestions = []
    
    if len(skills) < 10:
        suggestions.append("Add more industry-specific technical skills (Target at least 10+).")
    
    if "experience" not in text.lower():
        suggestions.append("Missing 'Experience' section. High priority for ATS.")
    
    if "education" not in text.lower():
        suggestions.append("Ensure your educational background is clearly documented.")
        
    weak_verbs = ["worked on", "responsible for", "helped", "assisted", "did"]
    for verb in weak_verbs:
        if verb in text.lower():
            suggestions.append(f"Upgrade '{verb}' to high-impact verbs like 'Spearheaded', 'Engineered', or 'Orchestrated'.")
            break
            
    return suggestions

def improve_bullet_point(point):
    point = point.strip()
    if not point: return None
    
    point_lower = point.lower()
    
    # 1. Calculate Bullet Impact Score (Out of 10)
    score = 4.0 # Base score
    
    # Add points for numbers/metrics
    if re.search(r'\d+%?', point):
        score += 2.5
        
    # Add points for strong verbs
    strong_verbs = ["spearheaded", "engineered", "orchestrated", "directed", "collaborated", "facilitated", "designed", "leveraged", "managed", "developed", "implemented", "optimized", "increased", "decreased", "reduced", "maximized"]
    if any(verb in point_lower for verb in strong_verbs):
        score += 2.0
    else:
        score -= 1.0 # Penalty for weak start
        
    # Length check
    words = point.split()
    if 10 <= len(words) <= 25:
        score += 1.5
    elif len(words) < 5:
        score -= 1.5
        
    score = max(1.0, min(10.0, round(score, 1)))
    
    # 2. General Rewrite
    patterns = [
        (r"(?i)\bi\s+worked\s+on\b", "Spearheaded the development of"),
        (r"(?i)\bworked\s+on\b", "Engineered and optimized"),
        (r"(?i)\bi\s+was\s+responsible\s+for\b", "Orchestrated key initiatives in"),
        (r"(?i)\bresponsible\s+for\b", "Directed operations for"),
        (r"(?i)\bi\s+helped\s+with\s+or\s+in\b", "Collaborated on the execution of"),
        (r"(?i)\bi\s+helped\b", "Facilitated improvements for"),
        (r"(?i)\bhelped\b", "Assisted in optimizing"),
        (r"(?i)\bi\s+did\b", "Successfully executed"),
        (r"(?i)\bmade\s+a\b", "Designed and implemented a"),
        (r"(?i)\bused\b", "Leveraged"),
        (r"(?i)\bhandled\b", "Managed complex")
    ]
    
    general_rewrite = point
    for pattern, replacement in patterns:
        general_rewrite = re.sub(pattern, replacement, general_rewrite)
        
    if general_rewrite == point and not re.match(r"(?i)^(" + "|".join(strong_verbs) + ")", point):
         general_rewrite = "Optimized " + point[0].lower() + point[1:]
         
    # 3. STAR Method Rewrite (Heuristic)
    star_rewrite = general_rewrite
    if "resulting in" not in star_rewrite.lower() and "improving" not in star_rewrite.lower():
        star_rewrite = general_rewrite.rstrip('.') + ", resulting in enhanced system stability and user engagement."
    else:
        star_rewrite = general_rewrite
        
    # 4. ATS Optimization (Heuristic adding keywords)
    ats_rewrite = star_rewrite.rstrip('.') + " by utilizing industry-standard technologies and agile methodologies."
    
    # Action Verb Suggestions
    action_verbs = ["Developed", "Implemented", "Designed", "Optimized", "Architected", "Accelerated", "Streamlined", "Pioneered"]
         
    return {
        "score": score,
        "general": general_rewrite,
        "star": star_rewrite,
        "ats": ats_rewrite,
        "action_verbs": action_verbs
    }

def get_score_category(score):
    if score >= 90: return "OUTSTANDING"
    if score >= 80: return "EXCELLENT"
    if score >= 60: return "VERY GOOD"
    if score >= 40: return "GOOD"
    if score >= 20: return "AVERAGE"
    return "WORST"

def check_grammar_communication(text):
    """Checks for common grammar mistakes and weak communication patterns."""
    issues = []
    text_lower = text.lower()
    
    # Common grammar errors
    grammar_patterns = [
        (r'\bi\s+is\b', "Grammar: 'I is' should be 'I am'"),
        (r'\btheir\s+is\b', "Grammar: 'their is' should be 'there is'"),
        (r'\byour\s+welcome\b', "Grammar: 'your welcome' should be 'you're welcome'"),
        (r'\bcould\s+of\b', "Grammar: 'could of' should be 'could have'"),
        (r'\bshould\s+of\b', "Grammar: 'should of' should be 'should have'"),
        (r'\bwould\s+of\b', "Grammar: 'would of' should be 'would have'"),
        (r'\bits\s+a\s+lot\b', "Minor: Consider if 'a lot' is professional enough for a resume"),
        (r'\balot\b', "Grammar: 'alot' is not a word — use 'a lot'"),
        (r'\bteh\b', "Typo: 'teh' should be 'the'"),
        (r'\brecieve\b', "Spelling: 'recieve' should be 'receive'"),
        (r'\boccured\b', "Spelling: 'occured' should be 'occurred'"),
        (r'\bseperate\b', "Spelling: 'seperate' should be 'separate'"),
        (r'\bdefinate\b', "Spelling: 'definate' should be 'definite'"),
        (r'\baccommodate\b', "Check: Ensure 'accommodate' is spelled correctly"),
        (r'\bmanagment\b', "Spelling: 'managment' should be 'management'"),
        (r'\bdevelopement\b', "Spelling: 'developement' should be 'development'"),
        (r'\benviroment\b', "Spelling: 'enviroment' should be 'environment'"),
    ]
    
    for pattern, msg in grammar_patterns:
        if re.search(pattern, text_lower):
            issues.append(msg)
    
    # Weak communication patterns
    weak_phrases = [
        ("i think", "Weak: Avoid 'I think' — state facts confidently"),
        ("i feel like", "Weak: Replace 'I feel like' with a definitive statement"),
        ("tried to", "Weak: 'Tried to' implies failure. Use 'Implemented' or 'Executed'"),
        ("was able to", "Weak: Remove 'was able to' and use direct verbs instead"),
        ("in charge of", "Weak: Replace 'in charge of' with 'Led', 'Managed', or 'Directed'"),
        ("worked with", "Weak: Replace 'worked with' with 'Collaborated', 'Partnered', or 'Coordinated'"),
        ("dealt with", "Weak: Replace 'dealt with' with 'Resolved', 'Addressed', or 'Managed'"),
        ("got", "Informal: Replace 'got' with 'Received', 'Achieved', or 'Obtained'"),
        ("stuff", "Informal: 'stuff' is unprofessional — use specific terminology"),
        ("things", "Vague: Replace 'things' with specific items or deliverables"),
        ("etc", "Vague: Avoid 'etc.' — list specific items or rephrase"),
        ("a lot of", "Vague: Replace 'a lot of' with specific quantities"),
        ("very", "Filler: Remove 'very' and use a stronger adjective"),
        ("really", "Filler: Remove 'really' — it weakens your statement"),
    ]
    
    for phrase, msg in weak_phrases:
        if phrase in text_lower:
            issues.append(msg)
    
    # Sentence structure checks
    sentences = re.split(r'[.!?]+', text)
    long_sentences = sum(1 for s in sentences if len(s.split()) > 30)
    if long_sentences > 2:
        issues.append(f"Readability: {long_sentences} sentences are too long (30+ words). Break them into shorter, punchier statements.")
    
    short_sentences = sum(1 for s in sentences if 2 < len(s.split()) < 5)
    if short_sentences > 5:
        issues.append(f"Readability: {short_sentences} sentences are too short. Combine or expand them for more impact.")
    
    # First person overuse
    first_person_count = len(re.findall(r'\bI\b', text))
    if first_person_count > 10:
        issues.append(f"Communication: Overuse of 'I' ({first_person_count} times). Start bullets with action verbs instead.")
    
    return issues

def calculate_ats_score(text, skills):
    """Calculates ATS (Applicant Tracking System) compatibility percentage."""
    ats_score = 0
    text_lower = text.lower()
    details = []
    
    # 1. Has proper sections (25 points)
    ats_sections = {
        'contact': ['email', 'phone', 'address', 'contact'],
        'experience': ['experience', 'work history', 'employment'],
        'education': ['education', 'academic', 'qualification'],
        'skills': ['skills', 'technical skills', 'competencies'],
    }
    section_score = 0
    for section_name, keywords in ats_sections.items():
        if any(kw in text_lower for kw in keywords):
            section_score += 6
        else:
            details.append(f"❌ Missing '{section_name.title()}' section")
    ats_score += min(section_score, 25)
    if section_score >= 24:
        details.append("✅ All key sections present")
    
    # 2. Keyword density (25 points)
    skill_count = len(skills)
    if skill_count >= 12:
        ats_score += 25
        details.append(f"✅ Strong keyword density ({skill_count} skills detected)")
    elif skill_count >= 8:
        ats_score += 18
        details.append(f"⚠️ Moderate keywords ({skill_count} skills — aim for 12+)")
    elif skill_count >= 4:
        ats_score += 10
        details.append(f"❌ Low keywords ({skill_count} skills — ATS needs 8+ minimum)")
    else:
        ats_score += 3
        details.append(f"🔴 Critical: Only {skill_count} skills found. ATS will likely reject.")
    
    # 3. Formatting compliance (20 points)
    format_score = 20
    if re.search(r'[│┃║▌▍▎▏]', text):  # Table/special chars
        format_score -= 5
        details.append("⚠️ Special characters detected — may confuse ATS parsers")
    if len(text.split('\n')) < 10:
        format_score -= 5
        details.append("⚠️ Very few line breaks — ATS may struggle to parse sections")
    ats_score += max(format_score, 0)
    if format_score >= 18:
        details.append("✅ Clean formatting for ATS")
    
    # 4. Contact information (15 points)
    contact_score = 0
    if re.search(r'[\w.+-]+@[\w-]+\.[\w.]+', text):
        contact_score += 5
    else:
        details.append("❌ No email address detected")
    if re.search(r'[\+]?\d[\d\s\-]{8,}', text):
        contact_score += 5
    else:
        details.append("❌ No phone number detected")
    if 'linkedin' in text_lower:
        contact_score += 5
    else:
        details.append("⚠️ No LinkedIn URL found")
    ats_score += contact_score
    
    # 5. Action verbs & quantification (15 points)
    action_verbs = ["developed", "managed", "led", "designed", "implemented", "created", 
                     "improved", "increased", "reduced", "built", "launched", "delivered",
                     "analyzed", "optimized", "collaborated", "architected", "streamlined"]
    verb_count = sum(1 for v in action_verbs if v in text_lower)
    if verb_count >= 5:
        ats_score += 15
        details.append(f"✅ Strong action verbs ({verb_count} found)")
    elif verb_count >= 3:
        ats_score += 10
        details.append(f"⚠️ Some action verbs ({verb_count}) — use more for impact")
    else:
        ats_score += 3
        details.append(f"❌ Weak action verbs ({verb_count}) — ATS favors strong verbs")
    
    if re.search(r'\d+%', text):
        details.append("✅ Quantified achievements found (percentages)")
    else:
        details.append("⚠️ No quantified results — add numbers/percentages")
    
    return min(ats_score, 100), details


def generate_backlogs(text, skills, target_role="General"):
    backlogs = []
    text_lower = text.lower()
    
    if len(skills) == 0: backlogs.append("No skills found.")
    elif len(skills) < 10: backlogs.append("Few skills will be learned; need more industry-relevant skills.")
    
    if "education" not in text_lower: backlogs.append("Education section missing.")
    if "experience" not in text_lower: backlogs.append("Experience section missing.")
    
    if not re.search(r'\b(cgpa|gpa|b\.tech|btech|bachelor)\b', text_lower):
        backlogs.append("B.Tech CGPA details missing.")
        
    if not re.search(r'\b(achievement|achievements|award|awards|certification|certifications)\b', text_lower):
        backlogs.append("Achievements and Certifications missing.")
        
    if "communication" not in text_lower and "leadership" not in text_lower:
        backlogs.append("Communication skills and soft skills not mentioned.")
        
    word_count = len(text.split())
    if word_count < 200: backlogs.append("Resume design: Content is too brief, lacks detail.")
    if word_count > 1000: backlogs.append("Resume design: Too lengthy, concisely summarize points.")
    
    # Targeted Skill Gap Analysis (Role-Specific)
    if target_role != "General" and target_role in DOMAINS_DB:
        reqs = DOMAINS_DB[target_role]
        missing_core = [r for r in reqs if r.lower() not in text_lower]
        for skill in missing_core:
            backlogs.append(f"CRITICAL GAP ({target_role}): Missing core requirement - {skill}")
    else:
        # General tech domain gaps
        tech_domains = {
            "Development": ["git", "html", "css", "javascript", "sql"],
            "Cloud/Infra": ["aws", "docker", "kubernetes", "linux"],
            "Data Science": ["python", "pandas", "machine learning"]
        }
        for domain, reqs in tech_domains.items():
            missing = [r for r in reqs if r not in text_lower]
            if len(missing) >= 2:
                backlogs.append(f"DOMAIN GAP: You are missing core {domain} skills like {', '.join(missing[:2])}.")
                
    return backlogs[:15] # Limit to top 15 most important backlogs

def extract_bullet_points(text):
    """
    Heuristically extracts bullet points or experience statements from the raw text.
    Handles different bullet characters like •, -, *, or line breaks following verbs.
    """
    lines = text.split('\n')
    bullets = []
    
    bullet_chars = ['•', '-', '*', '→', '', '✓']
    
    for line in lines:
        line = line.strip()
        if not line: continue
        
        # Strip common leading bullet bullet chars
        for char in bullet_chars:
            if line.startswith(char):
                line = line[1:].strip()
                break
                
        # Must be a reasonable length for an experience bullet point (avoiding headers/dates)
        if len(line.split()) >= 4 and len(line) > 15:
            # We want sentences that likely describe work, not random paragraphs
            # Basic heuristic: starts with uppercase letter or number, doesn't end in question mark.
            if re.match(r'^[A-Z0-9]', line) and not line.endswith('?'):
                bullets.append(line)
                
    return bullets[:50] # Limit to top 50 statements
