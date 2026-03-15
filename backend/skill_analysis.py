
import pandas as pd
import os

# ------------------ LOAD DATASET ------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "dataset", "dataset.csv")

df = pd.read_csv(DATA_PATH)

# Normalize column names (safety)
df.columns = df.columns.str.strip().str.lower()


# ------------------ ANALYSIS FUNCTION ------------------

def analyze_skills(user_skills, job_domain):

    # Validation
    if not job_domain:
        return [], 0

    if not isinstance(user_skills, list):
        user_skills = []


    # Filter dataset for selected job domain
    domain_data = df[
        df["job_domain"].str.lower() ==
        job_domain.lower()
    ]

    if domain_data.empty:
        return [], 0


    # Extract required skills from CSV
    required_skills = set()

    for skills in domain_data["it_skills"]:

        if pd.notna(skills):

            skill_list = [
                s.strip()
                for s in skills.split(",")
            ]

            required_skills.update(skill_list)


    # Normalize user skills
    user_skills_lower = [
        s.lower()
        for s in user_skills
    ]


    # Find missing skills
    missing_skills = [

        skill
        for skill in required_skills

        if skill.lower()
        not in user_skills_lower

    ]


    # Calculate progress percentage
    total_skills = len(required_skills)

    learned_skills = (
        total_skills - len(missing_skills)
    )

    progress = 0

    if total_skills > 0:

        progress = round(
            (learned_skills / total_skills) * 100,
            2
        )


    # return for routes.py
    return missing_skills, progress
