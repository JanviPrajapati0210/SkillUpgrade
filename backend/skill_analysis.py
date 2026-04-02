import pandas as pd
import os

from course_data import COURSES, skill_course_map


# ================= LOAD DATASET =================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "dataset", "dataset.csv")

df = pd.read_csv(DATA_PATH)
df.columns = df.columns.str.strip().str.lower()


# ================= ANALYSIS FUNCTION =================

def analyze_skills(user_skills, job_domain, level):

    # ---------- VALIDATION ----------

    if not job_domain:
        return [], 0, {}

    if isinstance(user_skills, str):
        user_skills = user_skills.split(",")

    if not isinstance(user_skills, list):
        user_skills = []

    user_skills_lower = [
        s.strip().lower() for s in user_skills if s.strip()
    ]

    if not level:
        level = "beginner"


    # ---------- FILTER DOMAIN ----------

    domain_data = df[
        df["job_domain"].str.lower() == job_domain.lower()
    ]

    if domain_data.empty:
        return [], 0, {}


    # ---------- REQUIRED SKILLS ----------

    required_skills = set()

    for skills in domain_data["it_skills"]:
        if pd.notna(skills):
            required_skills.update(
                [s.strip().lower() for s in skills.split(",")]
            )


    # ---------- MISSING SKILLS ----------

    missing = [
        s for s in required_skills
        if s not in user_skills_lower
    ]


    # ---------- PROGRESS ----------

    total = len(required_skills)
    learned = total - len(missing)

    progress = int((learned / total) * 100) if total > 0 else 0


    # ---------- ROADMAP (FINAL LOGIC ) ----------

    roadmap = {}

    for skill in missing:

        #  1. Exact mapping (BEST)
        if skill in skill_course_map:
            course = skill_course_map[skill]

            roadmap[skill] = {
                "title": course["course_name"],
                "link": course["link"]
            }

        #  2. COURSES fallback
        elif skill in COURSES:

            if isinstance(COURSES[skill], dict):

                if level in COURSES[skill]:
                    roadmap[skill] = COURSES[skill][level]
                else:
                    roadmap[skill] = list(COURSES[skill].values())[0]

            else:
                roadmap[skill] = COURSES[skill]

        # 3. Dynamic Coursera search (SMART fallback)
        else:
            search_url = f"https://www.coursera.org/search?query={skill.replace(' ', '%20')}"

            roadmap[skill] = {
                "title": f"Learn {skill}",
                "link": search_url
            }


    # ---------- RETURN ----------

    return missing, progress, roadmap