from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from logger import logger
from auth import register_user, login_user
from skill_analysis import analyze_skills
from db import get_db_connection

api = Blueprint("api", __name__)

# ------------------ AUTH ROUTES ------------------

@api.route("/register", methods=["POST"])
def register():
    logger.info("User registration attempted")

    response, status_code = register_user(request.json)
    return jsonify(response), status_code


@api.route("/login", methods=["POST"])
def login():
    logger.info("User login attempted")

    response, status_code = login_user(request.json)
    return jsonify(response), status_code


# ------------------ SKILL ANALYSIS ------------------

@api.route("/analyze-skills", methods=["POST"])
@jwt_required()
def analyze():
    current_user = get_jwt_identity()
    logger.info(f"Skill analysis requested by {current_user}")

    result = analyze_skills(request.json)
    return jsonify(result), 200


# ------------------ SAVE PROGRESS ------------------

@api.route("/save-progress", methods=["POST"])
@jwt_required()
def save_progress():
    user_email = get_jwt_identity()
    data = request.json

    skill = data.get("skill")
    progress = data.get("progress")

    if not skill or progress is None:
        return jsonify({"error": "Skill and progress are required"}), 400

    try:
        db = get_db_connection()
        cursor = db.cursor()

        cursor.execute("SELECT id FROM users WHERE email=%s", (user_email,))
        user = cursor.fetchone()

        if not user:
            return jsonify({"error": "User not found"}), 404

        user_id = user[0]

        cursor.execute("""
            INSERT INTO user_progress (user_id, skill_name, progress)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE progress=%s
        """, (user_id, skill, progress, progress))

        db.commit()

        logger.info(f"Progress saved for {user_email} - {skill}: {progress}%")
        return jsonify({"message": "Progress saved successfully"}), 201

    except Exception as e:
        logger.error(str(e))
        return jsonify({"error": "Database error"}), 500

