from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

# ------------------ LOAD ENV ------------------

load_dotenv()

# ------------------ CREATE APP ------------------

app = Flask(__name__)

# ------------------ CONFIG ------------------

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = int(
    os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 3600)
)

# ------------------ ENABLE CORS ------------------

CORS(app, supports_credentials=True)

# ------------------ INIT JWT ------------------

jwt = JWTManager(app)

# ------------------ REGISTER BLUEPRINT ------------------

from routes import api
app.register_blueprint(api, url_prefix="/api")

# ------------------ JWT ERROR HANDLERS ------------------

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({"error": "Token has expired"}), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({"error": "Invalid token"}), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({"error": "Authorization token is missing"}), 401


# ------------------ GLOBAL ERROR HANDLERS ------------------

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Route not found"}), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Internal server error"}), 500


# ------------------ TEST ROUTE ------------------

@app.route("/")
def home():
    return jsonify({
        "message": "SkillUpgrade Backend Running Successfully"
    })


# ------------------ RUN SERVER ------------------

if __name__ == "__main__":
    app.run(debug=True, port=5000)