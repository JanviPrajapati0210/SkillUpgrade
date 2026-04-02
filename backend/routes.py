from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from db import get_db_connection
from skill_analysis import analyze_skills

# ------------------ ML ------------------
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from course_data import courses

api = Blueprint("api", __name__)

# ------------------ ML SETUP ------------------

texts = [
    course["skills"] + " " + course["description"]
    for course in courses
]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

model = NearestNeighbors(n_neighbors=3, metric='cosine')
model.fit(X)

# all skills
all_skills = set()
for course in courses:
    for skill in course["skills"].split():
        all_skills.add(skill.lower())


# ------------------ AUTH ------------------

@api.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "All fields required"}), 400

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        if cursor.fetchone():
            return jsonify({"error": "Email exists"}), 409

        hashed = generate_password_hash(password)

        cursor.execute(
            "INSERT INTO users(email,password) VALUES(%s,%s)",
            (email, hashed)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Registered"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if not user or not check_password_hash(user["password"], password):
            return jsonify({"error": "Invalid login"}), 401

        token = create_access_token(identity=email)

        return jsonify({"access_token": token})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ------------------ ANALYZE ------------------

@api.route("/analyze-skills", methods=["POST"])
@jwt_required()
def analyze_user_skills():
    try:
        data = request.get_json()

        job_domain = data.get("job_domain")
        skills = data.get("skills")
        level = data.get("level")

        missing, progress, roadmap = analyze_skills(
            skills,
            job_domain,
            level
        )

        return jsonify({
            "missing_skills": missing,
            "progress": progress,
            "roadmap": roadmap
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ------------------ ML RECOMMENDATION ------------------

@api.route("/recommend-courses", methods=["POST"])
@jwt_required()
def recommend_courses():

    try:
        data = request.get_json()
        user_input = data.get("skills", "")

        skills_list = user_input.split(",")
        user_skills = set([s.strip().lower() for s in skills_list])

        cleaned_input = " ".join(user_skills)

        # -------- Missing Skills --------
        missing_skills = list(all_skills - user_skills)

        # -------- EXISTING SKILLS (ADVANCED - ML) --------
        existing_recommendations = []

        for skill in user_skills:
            skill_vector = vectorizer.transform([skill])
            distances, indices = model.kneighbors(skill_vector, n_neighbors=2)

            courses_list = []
            for i in indices[0]:
                courses_list.append({
                    "course_name": courses[i]["course_name"],
                    "link": courses[i]["link"]
                })

            existing_recommendations.append({
                "skill": skill,
                "recommended_courses": courses_list
            })

        # -------- MISSING SKILLS (LEARNING - ML) --------
        missing_recommendations = []

        for skill in missing_skills[:5]:
            skill_vector = vectorizer.transform([skill])
            distances, indices = model.kneighbors(skill_vector, n_neighbors=2)

            courses_list = []
            for i in indices[0]:
                courses_list.append({
                    "course_name": courses[i]["course_name"],
                    "link": courses[i]["link"]
                })

            missing_recommendations.append({
                "skill": skill,
                "recommended_courses": courses_list
            })

        return jsonify({
            "user_skills": list(user_skills),
            "missing_skills": missing_skills[:10],
            "existing_skill_courses": existing_recommendations,
            "missing_skill_courses": missing_recommendations
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
@api.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    return jsonify({
        "message": "Logged out successfully"
    })