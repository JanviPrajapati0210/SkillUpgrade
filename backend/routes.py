
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db_connection
from skill_analysis import analyze_skills

api = Blueprint("api", __name__)


# ------------------ REGISTER ------------------

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

        cursor.execute(
            "SELECT * FROM users WHERE email=%s",
            (email,)
        )

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


# ------------------ LOGIN ------------------

@api.route("/login", methods=["POST"])
def login():
    try:

        data = request.get_json()

        email = data.get("email")
        password = data.get("password")

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM users WHERE email=%s",
            (email,)
        )

        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if not user:
            return jsonify({"error": "Invalid login"}), 401

        if not check_password_hash(user["password"], password):
            return jsonify({"error": "Invalid login"}), 401

        token = create_access_token(identity=email)

        return jsonify({
            "access_token": token
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ------------------ PROFILE ------------------

@api.route("/profile", methods=["GET"])
@jwt_required()
def profile():

    try:

        email = get_jwt_identity()

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT id,email FROM users WHERE email=%s",
            (email,)
        )

        user = cursor.fetchone()

        cursor.close()
        conn.close()

        return jsonify(user), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ------------------ GET USERS ------------------

@api.route("/users", methods=["GET"])
@jwt_required()
def users():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id,email FROM users")

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(data)

# ------------------ ANALYZE SKILLS ------------------

@api.route("/analyze-skills", methods=["POST"])
@jwt_required()
def analyze_skills_route():

    try:

        data = request.get_json()

        job_domain = data.get("job_domain")
        skills = data.get("skills")

        email = get_jwt_identity()

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # get user id
        cursor.execute(
            "SELECT id FROM users WHERE email=%s",
            (email,)
        )

        user = cursor.fetchone()

        if not user:
            return jsonify({"error": "User not found"}), 404

        user_id = user["id"]

        # save domain
        cursor.execute(
            """
            INSERT INTO user_domains(user_id,job_domain)
            VALUES(%s,%s)
            """,
            (user_id, job_domain)
        )

        conn.commit()

        # ✅ FIX HERE
        missing, progress = analyze_skills(
            skills,
            job_domain
        )

        cursor.close()
        conn.close()

        return jsonify({
            "job_domain": job_domain,
            "missing_skills": missing,
            "known_skills": 0,
            "total_required_skills": 0,
            "progress_percentage": progress,
            "roadmap": {}
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ------------------ SAVE PROGRESS ------------------

@api.route("/save-progress", methods=["POST"])
@jwt_required()
def save_progress():

    try:

        data = request.get_json()

        skill = data.get("skill")
        progress = data.get("progress")

        email = get_jwt_identity()

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT id FROM users WHERE email=%s",
            (email,)
        )

        user = cursor.fetchone()

        if not user:
            return jsonify({"error": "User not found"}), 404

        user_id = user["id"]

        cursor.execute(
            """
            INSERT INTO user_progress
            (user_id, skill_name, progress)
            VALUES (%s,%s,%s)
            """,
            (user_id, skill, progress)
        )

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"message": "Progress saved"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500