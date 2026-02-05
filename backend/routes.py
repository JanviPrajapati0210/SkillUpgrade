from logger import logger
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from auth import register_user, login_user
from skill_analysis import analyze_skills

api = Blueprint("api", __name__)

@api.route("/register", methods=["POST"])
def register():
    logger.info("User registration attempted")
    return register_user(request.json)

@api.route("/login", methods=["POST"])
def login():
    logger.info("User login attempted")
    return login_user(request.json)

@api.route("/analyze-skills", methods=["POST"])
@jwt_required()
def analyze():
    logger.info("Skill analysis requested")
    return jsonify(analyze_skills(request.json))
