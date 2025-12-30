from flask import Flask, request, jsonify, render_template
import json

app = Flask(__name__)

# --- Your existing skill database and functions ---

# ADDITIONAL MULTI-DOMAIN SKILL DATABASES
skill_databases = {}
skill_databases.update({

    "Education Jobs": {
        "School Teacher": {"teaching", "lesson planning", "classroom management", "assessment", "communication"},
        "College Lecturer": {"subject expertise", "research", "presentation", "curriculum design", "evaluation"},
        "Professor": {"research", "phd", "publishing", "mentoring", "grant writing"},
        "Online Tutor": {"communication", "video tools", "subject expertise", "time management"},
        "Instructional Designer": {"curriculum design", "e-learning", "lms", "storyboarding", "assessment"},
        "Education Counselor": {"career guidance", "counseling", "psychology", "student assessment"},
        "Special Educator": {"special needs", "patience", "individual education plans", "therapy basics"},
        "Academic Coordinator": {"planning", "administration", "scheduling", "quality control"},
        "Exam Coordinator": {"evaluation", "invigilation", "compliance", "documentation"},
        "EdTech Product Manager": {"education domain", "product design", "analytics", "stakeholder management"}
    },

    "Engineering Jobs": {
        "Mechanical Engineer": {"cad", "thermodynamics", "manufacturing", "solidworks", "autocad"},
        "Civil Engineer": {"structural design", "construction", "surveying", "estimation", "autocad"},
        "Electrical Engineer": {"circuits", "power systems", "plc", "control systems"},
        "Electronics Engineer": {"embedded systems", "microcontrollers", "pcb design", "iot"},
        "Robotics Engineer": {"robotics", "automation", "python", "ros", "ai"},
        "Chemical Engineer": {"process design", "chemistry", "safety", "plant operations"},
        "Automobile Engineer": {"vehicle dynamics", "engines", "diagnostics", "cad"},
        "Aerospace Engineer": {"aerodynamics", "propulsion", "avionics", "simulation"},
        "Mechatronics Engineer": {"mechanical", "electronics", "automation", "control systems"},
        "Industrial Engineer": {"process optimization", "lean", "six sigma", "quality control"}
    },

    "Finance & Banking Jobs": {
        "Bank Clerk": {"account handling", "customer service", "banking operations"},
        "Loan Officer": {"credit analysis", "documentation", "risk assessment"},
        "Investment Banker": {"valuation", "m&a", "financial modeling", "pitch decks"},
        "Stock Trader": {"technical analysis", "market analysis", "risk management"},
        "Risk Manager": {"risk analysis", "compliance", "financial regulations"},
        "Insurance Advisor": {"policy knowledge", "sales", "customer relationship"},
        "Wealth Manager": {"portfolio management", "client advisory", "investment planning"},
        "Credit Analyst": {"credit scoring", "financial statements", "risk assessment"},
        "Treasury Analyst": {"cash flow", "liquidity management", "forecasting"},
        "Compliance Officer": {"regulatory compliance", "audit", "policy enforcement"}
    },

    "Government & Public Sector Jobs": {
        "IAS Officer": {"administration", "policy making", "public service"},
        "IPS Officer": {"law enforcement", "leadership", "investigation"},
        "Government Clerk": {"documentation", "data entry", "office procedures"},
        "Policy Analyst": {"policy research", "data analysis", "report writing"},
        "Urban Planner": {"city planning", "sustainability", "gis"},
        "Public Relations Officer": {"communication", "media handling", "public outreach"},
        "Revenue Officer": {"taxation", "land records", "compliance"},
        "Defense Officer": {"strategy", "leadership", "national security"},
        "Election Officer": {"election management", "compliance", "coordination"},
        "Public Health Officer": {"health policy", "epidemiology", "community programs"}
    },

    "Manufacturing & Industrial Jobs": {
        "Production Manager": {"production planning", "process control", "efficiency"},
        "Quality Engineer": {"quality assurance", "testing", "six sigma"},
        "Plant Manager": {"operations", "maintenance", "team management"},
        "Supply Chain Analyst": {"logistics", "forecasting", "inventory"},
        "Safety Officer": {"industrial safety", "compliance", "risk assessment"},
        "Maintenance Engineer": {"equipment maintenance", "troubleshooting"},
        "Tool Design Engineer": {"tooling", "cad", "manufacturing processes"},
        "Process Engineer": {"process optimization", "workflow design"},
        "Materials Engineer": {"material science", "testing", "failure analysis"},
        "Packaging Engineer": {"packaging design", "materials", "sustainability"}
    },

    "Media & Communication Jobs": {
        "Journalist": {"reporting", "writing", "investigation", "ethics"},
        "News Anchor": {"public speaking", "presentation", "communication"},
        "Public Relations Manager": {"media relations", "branding", "crisis management"},
        "Social Media Manager": {"content strategy", "analytics", "engagement"},
        "Digital Marketer": {"seo", "ads", "analytics", "campaigns"},
        "Radio Jockey": {"voice modulation", "entertainment", "communication"},
        "Podcast Producer": {"audio editing", "storytelling", "distribution"},
        "Media Planner": {"campaign planning", "budgeting", "analytics"},
        "Communications Strategist": {"messaging", "brand positioning"},
        "Corporate Spokesperson": {"public speaking", "media handling"}
    },

    "Logistics & Transportation Jobs": {
        "Logistics Manager": {"supply chain", "inventory", "transportation"},
        "Fleet Manager": {"vehicle management", "maintenance", "routing"},
        "Warehouse Manager": {"storage", "inventory control", "operations"},
        "Shipping Coordinator": {"documentation", "export import", "tracking"},
        "Customs Officer": {"customs regulations", "compliance"},
        "Procurement Manager": {"vendor management", "negotiation"},
        "Transport Planner": {"route planning", "optimization"},
        "Courier Operations Head": {"delivery management", "tracking"},
        "Freight Forwarder": {"logistics coordination", "documentation"},
        "Demand Planner": {"forecasting", "data analysis"}
    },

    "Sports & Fitness Jobs": {
        "Fitness Trainer": {"workout planning", "nutrition basics", "motivation"},
        "Sports Coach": {"training", "strategy", "team management"},
        "Physiotherapist (Sports)": {"rehabilitation", "injury prevention"},
        "Nutritionist": {"diet planning", "health science"},
        "Yoga Instructor": {"asana", "pranayama", "meditation"},
        "Sports Analyst": {"performance analysis", "statistics"},
        "Athletic Trainer": {"conditioning", "injury care"},
        "Referee": {"rules knowledge", "decision making"},
        "Sports Psychologist": {"mental training", "counseling"},
        "Gym Manager": {"operations", "customer management"}
    },
    "Software Jobs": {
        "Frontend Developer": {"html", "css", "javascript", "react", "angular", "vue", "typescript", "tailwind"},
        "Backend Developer": {"python", "django", "flask", "node.js", "sql", "api", "c#", "java", "spring", ".net"},
        "Data Scientist": {"python", "pandas", "numpy", "ml", "statistics", "sql", "scikit-learn", "tensorflow"},
        "DevOps Engineer": {"docker", "kubernetes", "aws", "jenkins", "linux", "ci/cd", "terraform", "ansible"},
        "Fullstack Developer": {"html", "css", "python", "react", "sql", "api", "javascript", "node.js"},
        "Mobile Developer": {"swift", "kotlin", "flutter", "react native", "java", "dart", "xcode", "android studio"},
        "Database Admin": {"sql", "mysql", "postgresql", "mongodb", "oracle", "redis", "backup", "performance tuning"},
        "QA Engineer": {"selenium", "testing", "pytest", "jira", "automation", "cypress", "postman", "load testing"},
        "Cloud Engineer": {"aws", "azure", "gcp", "terraform", "docker", "kubernetes", "serverless", "vpc"},
        "Cybersecurity": {"firewall", "encryption", "penetration", "network security", "siem", "ids/ips", "malware analysis"},
        "UI/UX Designer": {"figma", "sketch", "prototyping", "user research", "adobe xd", "wireframing", "usability"},
        "Blockchain Dev": {"solidity", "ethereum", "smart contracts", "web3", "rust", "hyperledger", "ipfs"}
    },
    "Healthcare Jobs": {
        "General Doctor": {"anatomy", "diagnosis", "medicine", "patient care", "medical ethics", "emergency response"},
        "Surgeon": {"surgery", "anatomy", "sterilization", "patient care", "surgical tools", "post-op care"},
        "Nurse": {"patient care", "medicine", "vital signs", "empathy", "wound care", "iv therapy", "catheterization"},
        "Pharmacist": {"medicine", "dosage", "pharmacy", "counseling", "drug interaction", "inventory management"},
        "Dentist": {"teeth", "oral surgery", "xray", "filling", "root canal", "braces", "periodontics"},
        "Radiologist": {"xray", "mri", "ct scan", "image analysis", "ultrasound", "pet scan", "radiology reporting"},
        "Physiotherapist": {"exercise", "rehabilitation", "muscle therapy", "electrotherapy", "manual therapy"},
        "Anesthesiologist": {"anesthesia", "pain management", "surgery support", "ventilation", "monitoring"},
        "Pediatrician": {"child care", "vaccination", "growth monitoring", "neonatology", "developmental assessment"},
        "Psychiatrist": {"mental health", "therapy", "medication", "counseling", "psychopharmacology", "crisis intervention"},
        "Lab Technician": {"blood test", "microscope", "sample analysis", "pcr", "centrifugation", "quality control"}
    },
    "Business Jobs": {
        "Marketing Manager": {"marketing", "social media", "analytics", "campaigns", "seo", "content strategy", "brand management"},
        "Sales Executive": {"communication", "negotiation", "sales", "relationship", "cold calling", "closing deals", "crm"},
        "Accountant": {"accounting", "taxes", "excel", "financial report", "gaap", "audit", "bookkeeping"},
        "HR Manager": {"recruitment", "training", "employee relations", "payroll", "performance review", "compliance"},
        "Financial Analyst": {"excel", "forecasting", "budgeting", "analysis", "valuation", "financial modeling", "tableau"},
        "Project Manager": {"planning", "team management", "budget", "timeline", "risk management", "agile", "scrum"},
        "Business Analyst": {"requirements", "process mapping", "stakeholder", "data analysis", "sql", "visio"},
        "Operations Manager": {"logistics", "supply chain", "process optimization", "inventory", "vendor management"},
        "Customer Support": {"communication", "problem solving", "empathy", "ticketing", "escalation", "documentation"},
        "Entrepreneur": {"business plan", "networking", "risk management", "fundraising", "pitching", "market research"},
        "Legal Advisor": {"contracts", "compliance", "regulations", "litigation", "corporate law", "intellectual property"}
    },
    "Creative Jobs": {
        "Graphic Designer": {"photoshop", "illustrator", "typography", "color theory", "indesign", "branding"},
        "Content Writer": {"writing", "seo", "research", "grammar", "copywriting", "blogging", "editing"},
        "Video Editor": {"premiere", "after effects", "color grading", "motion graphics", "davinci resolve", "sound editing"},
        "Photographer": {"photoshop", "lighting", "composition", "camera", "lens knowledge", "post processing"},
        "Animator": {"blender", "after effects", "3d modeling", "rigging", "maya", "unity", "keyframing"},
        "Fashion Designer": {"sketching", "sewing", "fabric knowledge", "trends", "pattern making", "draping"},
        "Interior Designer": {"space planning", "3d rendering", "color schemes", "autocad", "sketchup", "furniture design"},
        "Music Producer": {"ableton", "mixing", "mastering", "sound design", "fl studio", "logic pro", "synths"},
        "Architect": {"autocad", "3d modeling", "structural design", "revit", "bim", "sustainable design"},
        "Copywriter": {"advertising", "persuasive writing", "brand voice", "headlines", "a/b testing"},
        "Web Designer": {"figma", "html", "css", "user experience", "webflow", "responsive design"}
    }

})
def manual_set_intersection(student_skills, job_skills):
    """Manual set intersection"""
    
    student_set = set(student_skills)
    job_set = set(job_skills)
    common_skills = set()
    for skill in student_set:
        if skill in job_set:
            common_skills.add(skill)
    
    return common_skills

def skill_match_score(student_skills, job_skills, gpa):
    """Core scoring algorithm"""
    
    common_skills = manual_set_intersection(student_skills, job_skills)
    match_count = len(common_skills)
    total_job_skills = len(job_skills)
    if total_job_skills == 0:
        return 0
    skill_ratio = match_count / total_job_skills
    gpa_weight = gpa / 10.0  # Assuming GPA is out of 10
    score = skill_ratio * gpa_weight * 100
    
    return round(score, 1)

def merge(left, right):
    """Merge Sort helper"""
    
    result = []
    i,j = 0,0
    
    while (i < len(left) and j < len(right)):
        if (left[i][1] >= right[j][1]):
            result.append(left[i])
            i = i + 1
        else:
            result.append(right[j])
            j = j + 1
    
    result=result+left[i:]
    result=result+right[j:]
    return result

def merge_sort(scores):
    """Merge Sort - O(n log n)"""
    
    if (len(scores) <= 1):
        return scores
    mid = len(scores) // 2
    left = merge_sort(scores[:mid])
    right = merge_sort(scores[mid:])
    
    return merge(left, right)

def generate_recommendations(student, domain="Software Jobs"):
    """Generate top 3 recommendations per domain"""
    
    # Ensure the domain exists in the database, otherwise default
    if domain not in skill_databases:
        domain = "Software Jobs"
        
    job_roles = skill_databases[domain]
    scores = []
    
    for job, skills in job_roles.items():
        score = skill_match_score(student["skills"], skills, student["gpa"])
        scores.append((job, score))
    
    return merge_sort(scores)[:3]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    """API endpoint to get recommendations."""
    data = request.get_json()
    
    # Basic validation and data extraction
    name = data.get('name', 'User')
    skills = [s.strip().lower() for s in data.get('skills', '').split(',') if s.strip()]
    domain = data.get('domain', 'Software Jobs')
    try:
        gpa = float(data.get('gpa', 0))
    except (ValueError, TypeError):
        gpa = 0.0

    # Ensure GPA is in a 0-10 scale for the algorithm, assuming input is 0-4
    # The original algorithm seems to expect GPA out of 10.
    # We will scale it from a 4-point scale.
    gpa_scaled = (gpa / 4.0) * 10.0 if gpa <= 4.0 else gpa

    student_data = {
        "name": name,
        "skills": skills,
        "gpa": gpa_scaled 
    }
    
    recommendations = generate_recommendations(student_data, domain)
    
    # Format for JSON response
    formatted_recs = [{"title": job, "score": score} for job, score in recommendations]
    
    return jsonify({"recommendations": formatted_recs})

from serverless_wsgi import handle

def handler(event, context):
    return handle(app, event, context)
