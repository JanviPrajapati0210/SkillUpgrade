from flask import Blueprint, request, jsonify
from auth import register_user, login_user
from skill_analysis import analyze_skills

api = Blueprint("api", __name__)

@api.route("/test", methods=["GET"])
def test():
    return {"message": "Routes working"}

@api.route("/register", methods=["POST"])
def register():
    data = request.json
    return register_user(data)

@api.route("/login", methods=["POST"])
def login():
    data = request.json
    return login_user(data)

@api.route("/analyze-skills", methods=["POST"])
def analyze():
    data = request.json
    return jsonify(analyze_skills(data))