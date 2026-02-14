import csv
import mysql.connector

# =========================
# Database Configuration
# =========================
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "JanviVidhi217",
    "database": "skillupgrade"
}

# =========================
# Connect to MySQL
# =========================
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# =========================
# Helper Functions
# =========================
def get_or_create_skill(skill_name, skill_type):
    skill_name = skill_name.strip().lower()

    cursor.execute(
        "SELECT skill_id FROM skills WHERE skill_name = %s",
        (skill_name,)
    )
    result = cursor.fetchone()

    if result:
        return result[0]

    cursor.execute(
        "INSERT INTO skills (skill_name, skill_type) VALUES (%s, %s)",
        (skill_name, skill_type)
    )
    conn.commit()
    return cursor.lastrowid


# =========================
# Load CSV Data
# =========================
csv_file = "SkillUpgrade_Jobs_Cleaned.csv"

with open(csv_file, newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        job_domain = row["job_domain"].strip()
        job_title = row["job_title"].strip()
        skill_level = row["skill_level"].strip().lower()

        # Insert Job
        cursor.execute(
            """
            INSERT INTO jobs (job_domain, job_title, skill_level)
            VALUES (%s, %s, %s)
            """,
            (job_domain, job_title, skill_level)
        )
        conn.commit()
        job_id = cursor.lastrowid

        # =========================
        # IT Skills
        # =========================
        it_skills = row["it_skills"].split(",")

        for skill in it_skills:
            if skill.strip():
                skill_id = get_or_create_skill(skill, "technical")
                cursor.execute(
                    "INSERT IGNORE INTO job_skills (job_id, skill_id) VALUES (%s, %s)",
                    (job_id, skill_id)
                )

        # =========================
        # Soft Skills
        # =========================
        soft_skills = row["soft_skills"].split(",")

        for skill in soft_skills:
            if skill.strip():
                skill_id = get_or_create_skill(skill, "soft")
                cursor.execute(
                    "INSERT IGNORE INTO job_skills (job_id, skill_id) VALUES (%s, %s)",
                    (job_id, skill_id)
                )

        conn.commit()

print("✅ Dataset successfully loaded into SkillUpgrade database!")


# Close Connection

cursor.close()
conn.close()
