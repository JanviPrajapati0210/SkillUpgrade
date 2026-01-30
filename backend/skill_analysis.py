
industry_skills = {
    "Python": "Learn basics, OOP, and libraries",
    "SQL": "Practice joins, queries, and indexing",
    "Data Structures": "Focus on arrays, stacks, queues",
    "Machine Learning": "Start with regression and classification"
}

def analyze_skills(data):
    user_skills = data.get("skills", [])

    missing = []
    roadmap = {}

    for skill, plan in industry_skills.items():
        if skill not in user_skills:
            missing.append(skill)
            roadmap[skill] = plan

    return {
        "missing_skills": missing,
        "roadmap": roadmap,
        "message": "Personalized learning roadmap generated"
    }

