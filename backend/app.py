from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)

# Configuration


app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "super-secret-key")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 3600  # 1 hour token validity

# Enable CORS (allow frontend connection)
CORS(app, resources={r"/*": {"origins": "*"}})

# Initialize JWT
jwt = JWTManager(app)


# Import and Register Blueprint

from routes import api  # Make sure blueprint name is "api"

app.register_blueprint(api, url_prefix="/api")


# JWT Error Handlers


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({
        "error": "Token has expired"
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        "error": "Invalid token"
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        "error": "Authorization token is missing"
    }), 401



# Global Error Handlers


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Route not found"
    }), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "error": "Internal server error"
    }), 500



# Test Route


@app.route("/")
def home():
    return jsonify({
        "message": "SkillUpgrade Backend Running Successfully"
    })



# Run Server

if __name__ == "__main__":
    app.run(debug=True)


