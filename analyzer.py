import re


# ==========================================
# SKILL DATABASE
# ==========================================

SKILLS = {

    "Programming": [
        "python",
        "java",
        "javascript",
        "c++",
        "c",
        "sql",
        "html",
        "css"
    ],

    "Data & Analytics": [
        "excel",
        "power bi",
        "tableau",
        "pandas",
        "numpy",
        "data analysis",
        "data visualization"
    ],

    "Electronics": [
        "arduino",
        "esp32",
        "esp8266",
        "raspberry pi",
        "microcontroller",
        "embedded systems",
        "electronics",
        "circuit design"
    ],

    "Robotics": [
        "robotics",
        "ros",
        "robot operating system",
        "automation",
        "robot programming",
        "sensors",
        "actuators"
    ],

    "Professional": [
        "communication",
        "leadership",
        "teamwork",
        "problem solving",
        "project management",
        "management",
        "teaching",
        "training",
        "research"
    ]

}


# ==========================================
# JOB REQUIREMENTS
# ==========================================

JOB_REQUIREMENTS = {

    "Software Developer": [
        "python",
        "javascript",
        "sql",
        "html",
        "css",
        "problem solving"
    ],

    "Data Analyst": [
        "python",
        "sql",
        "excel",
        "power bi",
        "data analysis",
        "data visualization"
    ],

    "Electronics Engineer": [
        "electronics",
        "microcontroller",
        "circuit design",
        "embedded systems",
        "arduino",
        "c"
    ],

    "Robotics Engineer": [
        "robotics",
        "python",
        "c++",
        "arduino",
        "sensors",
        "automation",
        "microcontroller"
    ],

    "Project Coordinator": [
        "communication",
        "leadership",
        "teamwork",
        "project management",
        "management",
        "problem solving"
    ],

    "Academic Coordinator": [
        "communication",
        "leadership",
        "teaching",
        "training",
        "management",
        "teamwork"
    ]

}


# ==========================================
# CAREER RECOMMENDATION DATABASE
# ==========================================

CAREER_RECOMMENDATIONS = {

    "Robotics Engineer": [
        "robotics",
        "python",
        "c++",
        "arduino",
        "sensors",
        "automation",
        "microcontroller"
    ],

    "Embedded Systems Engineer": [
        "embedded systems",
        "microcontroller",
        "c",
        "c++",
        "arduino",
        "esp32",
        "electronics"
    ],

    "Electronics Engineer": [
        "electronics",
        "circuit design",
        "microcontroller",
        "arduino",
        "embedded systems",
        "c"
    ],

    "Automation Engineer": [
        "automation",
        "robotics",
        "sensors",
        "actuators",
        "microcontroller",
        "electronics"
    ],

    "Software Developer": [
        "python",
        "java",
        "javascript",
        "sql",
        "html",
        "css",
        "problem solving"
    ],

    "Data Analyst": [
        "python",
        "sql",
        "excel",
        "power bi",
        "tableau",
        "pandas",
        "numpy",
        "data analysis",
        "data visualization"
    ],

    "Project Coordinator": [
        "communication",
        "leadership",
        "teamwork",
        "project management",
        "management",
        "problem solving"
    ],

    "Academic Coordinator": [
        "communication",
        "leadership",
        "teaching",
        "training",
        "management",
        "teamwork"
    ],

    "Technical Trainer": [
        "teaching",
        "training",
        "communication",
        "robotics",
        "electronics",
        "programming"
    ],

    "Research Assistant": [
        "research",
        "python",
        "data analysis",
        "electronics",
        "robotics",
        "problem solving"
    ]

}


# ==========================================
# NORMALIZE TEXT
# ==========================================

def normalize_text(text):

    text = text.lower()

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text


# ==========================================
# DETECT SKILLS
# ==========================================

def detect_skills(text):

    text = normalize_text(text)

    detected = []

    for category, skills in SKILLS.items():

        for skill in skills:

            if skill in text:

                detected.append({
                    "skill": skill,
                    "category": category
                })

    return detected


# ==========================================
# DETECT EDUCATION
# ==========================================

def detect_education(text):

    text = normalize_text(text)

    education_keywords = [

        "phd",
        "ph.d",
        "doctorate",

        "master",
        "msc",
        "m.sc",
        "mtech",
        "m.tech",
        "mba",

        "bachelor",
        "bsc",
        "b.sc",
        "btech",
        "b.tech",
        "be",

        "diploma",

        "higher secondary",
        "plus two",
        "12th",
        "10th",
        "secondary school"

    ]

    found = []

    for keyword in education_keywords:

        if keyword in text:

            found.append(keyword)

    return list(dict.fromkeys(found))


# ==========================================
# DETECT EXPERIENCE
# ==========================================

def detect_experience(text):

    text = normalize_text(text)

    experience_patterns = [

        r"(\d+)\+?\s*years?\s*(?:of\s*)?experience",

        r"(\d+)\+?\s*years?\s*working",

        r"(\d+)\+?\s*years?\s*in"

    ]

    years = []

    for pattern in experience_patterns:

        matches = re.findall(
            pattern,
            text
        )

        years.extend(matches)

    if years:

        numbers = [
            int(year)
            for year in years
        ]

        return max(numbers)

    return 0


# ==========================================
# JOB MATCHING
# ==========================================

def analyze_job_match(
    detected_skills,
    target_job
):

    detected_skill_names = [

        item["skill"]

        for item in detected_skills

    ]

    required_skills = JOB_REQUIREMENTS.get(
        target_job,
        []
    )

    matched = []
    missing = []

    for skill in required_skills:

        if skill in detected_skill_names:

            matched.append(skill)

        else:

            missing.append(skill)

    if required_skills:

        score = round(
            (len(matched) / len(required_skills)) * 100
        )

    else:

        score = 0

    return {

        "score": score,

        "matched": matched,

        "missing": missing

    }


# ==========================================
# CAREER RECOMMENDATIONS
# ==========================================

def generate_career_recommendations(
    detected_skills
):

    detected_skill_names = {

        item["skill"]

        for item in detected_skills

    }

    recommendations = []

    for career, required_skills in CAREER_RECOMMENDATIONS.items():

        matched = [

            skill

            for skill in required_skills

            if skill in detected_skill_names

        ]

        if required_skills:

            score = round(
                (len(matched) / len(required_skills)) * 100
            )

        else:

            score = 0

        recommendations.append({

            "career": career,

            "score": score,

            "matched_skills": matched,

            "required_skills": required_skills

        })

    recommendations.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return recommendations[:5]


# ==========================================
# ATS SCORE
# ==========================================

def calculate_ats_score(
    resume_text,
    detected_skills,
    job_match,
    education,
    experience
):

    text = normalize_text(resume_text)

    score = 0

    # JOB SKILL MATCH

    score += round(
        job_match["score"] * 0.50
    )

    # EDUCATION

    if education:

        score += 15

    # EXPERIENCE

    if experience > 0:

        score += 15

    # RESUME SECTIONS

    sections = [

        "education",
        "experience",
        "skills",
        "project",
        "projects",
        "summary",
        "objective"

    ]

    sections_found = 0

    for section in sections:

        if section in text:

            sections_found += 1

    section_score = min(
        sections_found * 2,
        10
    )

    score += section_score

    # SKILLS BONUS

    if len(detected_skills) >= 5:

        score += 10

    elif len(detected_skills) >= 3:

        score += 5

    return min(score, 100)


# ==========================================
# EDUCATION ANALYSIS
# ==========================================

def analyze_education(education):

    if not education:

        return {

            "status": "Not detected",

            "message":
                "No clear educational qualification "
                "was detected in the resume."

        }

    highest = education[0]

    if any(

        item in education

        for item in [

            "phd",
            "ph.d",
            "doctorate"

        ]

    ):

        highest = "PhD / Doctorate"

    elif any(

        item in education

        for item in [

            "master",
            "msc",
            "m.sc",
            "mtech",
            "m.tech",
            "mba"

        ]

    ):

        highest = "Postgraduate"

    elif any(

        item in education

        for item in [

            "bachelor",
            "bsc",
            "b.sc",
            "btech",
            "b.tech",
            "be"

        ]

    ):

        highest = "Undergraduate"

    elif "diploma" in education:

        highest = "Diploma"

    return {

        "status": "Detected",

        "highest": highest,

        "message":
            "Educational qualification detected "
            "in the resume."

    }


# ==========================================
# EXPERIENCE ANALYSIS
# ==========================================

def analyze_experience(experience):

    if experience == 0:

        return {

            "level": "Entry Level",

            "message":
                "No clear professional experience "
                "was detected."

        }

    if experience < 2:

        level = "Early Career"

    elif experience < 5:

        level = "Mid Level"

    else:

        level = "Experienced Professional"

    return {

        "level": level,

        "years": experience,

        "message":
            f"Approximately {experience} "
            f"year(s) of experience detected."

    }


# ==========================================
# RESUME STRENGTHS
# ==========================================

def generate_strengths(
    resume_text,
    detected_skills,
    education,
    experience,
    job_match
):

    text = normalize_text(resume_text)

    strengths = []

    if len(detected_skills) >= 5:

        strengths.append(
            "Strong range of relevant skills detected."
        )

    elif len(detected_skills) >= 3:

        strengths.append(
            "Several relevant skills are included."
        )

    if education:

        strengths.append(
            "Educational qualification is included."
        )

    if experience > 0:

        strengths.append(
            "Professional experience is present."
        )

    if job_match["score"] >= 70:

        strengths.append(
            "Good alignment with the selected target job."
        )

    if "project" in text or "projects" in text:

        strengths.append(
            "Projects are mentioned in the resume."
        )

    if "certification" in text or "certifications" in text:

        strengths.append(
            "Certifications are included."
        )

    if not strengths:

        strengths.append(
            "The resume provides a starting point "
            "for improvement."
        )

    return strengths


# ==========================================
# WEAK AREAS
# ==========================================

def generate_weaknesses(
    resume_text,
    detected_skills,
    education,
    experience,
    job_match
):

    text = normalize_text(resume_text)

    weaknesses = []

    if job_match["missing"]:

        weaknesses.append(
            "Some important skills required for "
            "the target job are missing."
        )

    if not education:

        weaknesses.append(
            "Education details were not clearly detected."
        )

    if experience == 0:

        weaknesses.append(
            "Professional experience was not clearly detected."
        )

    if "project" not in text and "projects" not in text:

        weaknesses.append(
            "Projects section is missing or unclear."
        )

    if "summary" not in text and "objective" not in text:

        weaknesses.append(
            "A professional summary or objective "
            "could be added."
        )

    if len(detected_skills) < 3:

        weaknesses.append(
            "The resume contains relatively few "
            "detectable skills."
        )

    return weaknesses


# ==========================================
# IMPROVEMENT SUGGESTIONS
# ==========================================

def generate_suggestions(
    weaknesses,
    job_match,
    experience
):

    suggestions = []

    if job_match["missing"]:

        missing = ", ".join(
            job_match["missing"][:4]
        )

        suggestions.append(
            f"Consider developing these target-job skills: "
            f"{missing}."
        )

    if experience == 0:

        suggestions.append(
            "Add internships, academic projects, "
            "freelance work, or practical experience "
            "to demonstrate your abilities."
        )

    if not weaknesses:

        suggestions.append(
            "Keep your resume updated with recent "
            "projects, skills, and achievements."
        )

    suggestions.append(
        "Use clear section headings such as "
        "Summary, Skills, Experience, Education, "
        "and Projects."
    )

    suggestions.append(
        "Use measurable achievements wherever "
        "possible instead of only listing duties."
    )

    return suggestions


# ==========================================
# CAREER ROADMAP DATABASE
# ==========================================

ROADMAP_DATA = {

    "python": {

        "title": "Learn Python",

        "level": "Beginner",

        "action":
            "Learn Python fundamentals, functions, "
            "lists, dictionaries and file handling.",

        "project":
            "Build a Resume Analyzer or Personal "
            "Expense Tracker."

    },

    "javascript": {

        "title": "Learn JavaScript",

        "level": "Beginner",

        "action":
            "Learn variables, functions, arrays, "
            "objects, DOM and events.",

        "project":
            "Build an interactive portfolio or "
            "task management application."

    },

    "sql": {

        "title": "Learn SQL",

        "level": "Beginner",

        "action":
            "Learn SELECT, WHERE, JOIN, GROUP BY "
            "and database design.",

        "project":
            "Build a Student Management Database."

    },

    "html": {

        "title": "Improve HTML",

        "level": "Beginner",

        "action":
            "Learn semantic HTML, forms, tables "
            "and accessible page structure.",

        "project":
            "Create a professional portfolio website."

    },

    "css": {

        "title": "Improve CSS",

        "level": "Beginner",

        "action":
            "Learn Flexbox, Grid, responsive design, "
            "animations and modern layouts.",

        "project":
            "Create a responsive dashboard interface."

    },

    "c++": {

        "title": "Learn C++",

        "level": "Beginner",

        "action":
            "Learn C++ syntax, functions, classes, "
            "pointers and object-oriented programming.",

        "project":
            "Build a sensor-based robotics project "
            "using C++."

    },

    "arduino": {

        "title": "Learn Arduino",

        "level": "Beginner",

        "action":
            "Learn Arduino programming, digital "
            "and analog sensors and motor control.",

        "project":
            "Build an automatic obstacle-avoiding robot."

    },

    "microcontroller": {

        "title": "Learn Microcontrollers",

        "level": "Intermediate",

        "action":
            "Understand microcontroller architecture, "
            "GPIO, timers, communication protocols "
            "and interrupts.",

        "project":
            "Build an ESP32-based smart automation system."

    },

    "embedded systems": {

        "title": "Learn Embedded Systems",

        "level": "Intermediate",

        "action":
            "Study embedded C/C++, microcontrollers, "
            "communication protocols and hardware-software "
            "integration.",

        "project":
            "Build a sensor monitoring system using ESP32."

    },

    "robotics": {

        "title": "Strengthen Robotics",

        "level": "Intermediate",

        "action":
            "Learn robot mechanics, sensors, actuators, "
            "control systems and robot programming.",

        "project":
            "Build an autonomous mobile robot."

    },

    "ros": {

        "title": "Learn ROS",

        "level": "Intermediate",

        "action":
            "Learn ROS nodes, topics, services, packages "
            "and robot simulation.",

        "project":
            "Create a simulated mobile robot using ROS."

    },

    "sensors": {

        "title": "Learn Sensor Integration",

        "level": "Beginner",

        "action":
            "Understand different sensors, signal reading "
            "and microcontroller integration.",

        "project":
            "Build a multi-sensor smart monitoring system."

    },

    "automation": {

        "title": "Learn Automation",

        "level": "Intermediate",

        "action":
            "Learn automation concepts, control systems, "
            "sensors and programmable controllers.",

        "project":
            "Build an automated home or industrial prototype."

    },

    "excel": {

        "title": "Improve Excel",

        "level": "Beginner",

        "action":
            "Learn formulas, pivot tables, charts, "
            "filtering and data cleaning.",

        "project":
            "Create an interactive business analytics dashboard."

    },

    "power bi": {

        "title": "Learn Power BI",

        "level": "Intermediate",

        "action":
            "Learn Power Query, data modelling, DAX "
            "and dashboard design.",

        "project":
            "Create a sales or HR analytics dashboard."

    },

    "data analysis": {

        "title": "Learn Data Analysis",

        "level": "Intermediate",

        "action":
            "Learn data cleaning, exploratory analysis, "
            "statistics and visualization.",

        "project":
            "Analyze a real-world public dataset."

    },

    "communication": {

        "title": "Improve Communication",

        "level": "Beginner",

        "action":
            "Practice professional writing, presentations, "
            "active listening and workplace communication.",

        "project":
            "Prepare and deliver a professional presentation."

    },

    "leadership": {

        "title": "Develop Leadership",

        "level": "Intermediate",

        "action":
            "Develop delegation, decision-making, conflict "
            "management and team coordination skills.",

        "project":
            "Lead a small team project from planning to completion."

    },

    "project management": {

        "title": "Learn Project Management",

        "level": "Intermediate",

        "action":
            "Learn project planning, task management, "
            "risk management and reporting.",

        "project":
            "Manage a complete project using a project management board."

    },

    "teaching": {

        "title": "Strengthen Teaching Skills",

        "level": "Intermediate",

        "action":
            "Improve lesson planning, classroom management, "
            "mentoring and assessment techniques.",

        "project":
            "Design and conduct a complete technical workshop."

    },

    "research": {

        "title": "Strengthen Research Skills",

        "level": "Intermediate",

        "action":
            "Learn research methodology, literature review, "
            "data collection and technical writing.",

        "project":
            "Complete a small research-based technical project."

    }

}


# ==========================================
# GENERATE CAREER ROADMAP
# ==========================================

def generate_career_roadmap(
    job_match,
    target_job
):

    missing_skills = job_match["missing"]

    roadmap = []

    # ADD MISSING SKILLS

    for skill in missing_skills:

        if skill in ROADMAP_DATA:

            roadmap.append({

                "skill": skill,

                "title":
                    ROADMAP_DATA[skill]["title"],

                "level":
                    ROADMAP_DATA[skill]["level"],

                "action":
                    ROADMAP_DATA[skill]["action"],

                "project":
                    ROADMAP_DATA[skill]["project"]

            })

    # DEFAULT ROADMAP

    if not roadmap:

        roadmap.append({

            "skill": "career",

            "title":
                f"Prepare for {target_job}",

            "level":
                "Next Step",

            "action":
                "Continue strengthening your existing skills "
                "and gain practical experience relevant to "
                "the target role.",

            "project":
                "Build a portfolio project directly related "
                "to your target job."

        })

    return roadmap


# ==========================================
# MAIN ANALYSIS FUNCTION
# ==========================================

def analyze_resume(
    resume_text,
    target_job
):

    # Detect skills

    detected_skills = detect_skills(
        resume_text
    )

    # Detect education

    education = detect_education(
        resume_text
    )

    # Detect experience

    experience = detect_experience(
        resume_text
    )

    # Match target job

    job_match = analyze_job_match(
        detected_skills,
        target_job
    )

    # Career recommendations

    career_recommendations = generate_career_recommendations(
        detected_skills
    )

    # Career roadmap

    career_roadmap = generate_career_roadmap(
        job_match,
        target_job
    )

    # Education analysis

    education_analysis = analyze_education(
        education
    )

    # Experience analysis

    experience_analysis = analyze_experience(
        experience
    )

    # ATS score

    ats_score = calculate_ats_score(
        resume_text,
        detected_skills,
        job_match,
        education,
        experience
    )

    # Strengths

    strengths = generate_strengths(
        resume_text,
        detected_skills,
        education,
        experience,
        job_match
    )

    # Weaknesses

    weaknesses = generate_weaknesses(
        resume_text,
        detected_skills,
        education,
        experience,
        job_match
    )

    # Suggestions

    suggestions = generate_suggestions(
        weaknesses,
        job_match,
        experience
    )

    return {

        "skills": detected_skills,

        "education": education,

        "education_analysis":
            education_analysis,

        "experience": experience,

        "experience_analysis":
            experience_analysis,

        "job_match": job_match,

        "ats_score": ats_score,

        "strengths": strengths,

        "weaknesses": weaknesses,

        "suggestions": suggestions,

        "career_roadmap": career_roadmap,

        "career_recommendations":
            career_recommendations

    }