
industry_skills = ["Python", "SQL", "Data Structures", "Machine Learning"]

def analyze_skills(data):
    user_skills = data.get("skills", [])

    missing_skills = []
    for skill in industry_skills:
        if skill not in user_skills:
            missing_skills.append(skill)

    return {
        "user_skills": user_skills,
        "missing_skills": missing_skills,
        "recommendation": "Focus on missing skills to improve employability"
    }
