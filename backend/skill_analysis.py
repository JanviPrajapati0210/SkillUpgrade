import pandas as pd
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "dataset", "dataset.csv")

df = pd.read_csv(DATA_PATH)


def analyze_skills(data):
    job_domain = data.get("job_domain")
    user_skills = data.get("skills", [])

    if not job_domain:
        return {"error": "Job domain is required"}

    domain_data = df[df["job_domain"].str.lower() == job_domain.lower()]

    if domain_data.empty:
        return {"error": "Invalid job domain"}

    
    required_skills = set()

    for skills in domain_data["it_skills"]:
        if pd.notna(skills):
            skill_list = [s.strip() for s in skills.split(",")]
            required_skills.update(skill_list)

    
    missing_skills = [
        skill for skill in required_skills
        if skill.lower() not in [s.lower() for s in user_skills]
    ]

    roadmap = {
        skill: f"Learn and practice {skill} through online courses and projects."
        for skill in missing_skills
    }

    return {
        "job_domain": job_domain,
        "missing_skills": missing_skills,
        "roadmap": roadmap,
        "message": "Personalized learning roadmap generated"
    }
