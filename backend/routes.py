from logger import logger
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from auth import register_user, login_user
from skill_analysis import analyze_skills

api = Blueprint("api", __name__)

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


@api.route("/analyze-skills", methods=["POST"])
@jwt_required()
def analyze():
    current_user = get_jwt_identity()
    logger.info(f"Skill analysis requested by {current_user}")

    result = analyze_skills(request.json)

    return jsonify(result), 200
