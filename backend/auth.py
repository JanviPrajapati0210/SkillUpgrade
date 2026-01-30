import hashlib
from flask_jwt_extended import create_access_token
from db import get_db_connection

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(data):
    email = data.get("email")
    password = hash_password(data.get("password"))

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    if cursor.fetchone():
        return {"message": "User already exists"}, 400

    cursor.execute(
        "INSERT INTO users (email, password) VALUES (%s, %s)",
        (email, password)
    )
    db.commit()

    return {"message": "User registered successfully"}, 201

def login_user(data):
    email = data.get("email")
    password = hash_password(data.get("password"))

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email=%s AND password=%s",
        (email, password)
    )

    user = cursor.fetchone()
    if not user:
        return {"message": "Invalid credentials"}, 401

    token = create_access_token(identity=email)
    return {"access_token": token}, 200