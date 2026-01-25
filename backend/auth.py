from flask_jwt_extended import create_access_token
import hashlib


users = {}

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(data):
    email = data.get("email")
    password = data.get("password")

    if email in users:
        return {"message": "User already exists"}, 400

    users[email] = hash_password(password)
    return {"message": "User registered successfully"}, 201

def login_user(data):
    email = data.get("email")
    password = data.get("password")

    if email not in users:
        return {"message": "User not found"}, 404

    if users[email] != hash_password(password):
        return {"message": "Invalid credentials"}, 401

    token = create_access_token(identity=email)
    return {"access_token": token}, 200