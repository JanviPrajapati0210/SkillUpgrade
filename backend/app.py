from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from routes import api
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY", "default_secret")
jwt = JWTManager(app)

app.register_blueprint(api)

@app.route("/")
def home():
    return {"message": "SkillUpgrade Backend Running Successfully"}

if __name__ == "__main__":
    app.run(debug=True)