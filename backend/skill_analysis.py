import pandas as pd
import os

from course_data import COURSES


# ================= LOAD DATASET =================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(BASE_DIR, "dataset","dataset.csv")

df = pd.read_csv(DATA_PATH)

df.columns = df.columns.str.strip().str.lower()


# ================= ANALYSIS FUNCTION =================

def analyze_skills(user_skills, job_domain, level):

    if not job_domain:
        return [], 0, {}

    if not isinstance(user_skills, list):
        user_skills = []

    if not level:
        level = "beginner"


    # ---------- filter domain ----------

    domain_data = df[
        df["job_domain"].str.lower()
        == job_domain.lower()
    ]

    if domain_data.empty:
        return [], 0, {}


    # ---------- required skills ----------

    required_skills = set()

    for skills in domain_data["it_skills"]:

        if pd.notna(skills):

            required_skills.update(
                [
                    s.strip().lower()
                    for s in skills.split(",")
                ]
            )


    # ---------- user skills ----------

    user_skills_lower = [
        s.lower()
        for s in user_skills
    ]


    # ---------- missing ----------

    missing = [

        s
        for s in required_skills
        if s not in user_skills_lower

    ]


    # ---------- progress ----------

    total = len(required_skills)

    learned = total - len(missing)

    progress = 0

    if total > 0:
        progress = int(
            (learned / total) * 100
        )


    # ---------- roadmap ----------

    roadmap = {}

    for skill in missing:

        if skill in COURSES:

            if level in COURSES[skill]:

                roadmap[skill] = \
                    COURSES[skill][level]

            else:

                roadmap[skill] = \
                    list(
                        COURSES[skill].values()
                    )[0]

        else:

            roadmap[skill] = {

                "title":
                f"Learn {skill}",

                "link":
                "https://www.coursera.org/"
            }


    return missing, progress, roadmap