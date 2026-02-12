from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db_connection


# Register User

def register_user(data):
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return {"message": "Email and password required"}, 400

    hashed_password = generate_password_hash(password)

    db = get_db_connection()
    cursor = db.cursor()

    # Check if user exists
    cursor.execute("SELECT id FROM users WHERE email=%s", (email,))
    if cursor.fetchone():
        return {"message": "User already exists"}, 400

    # Insert new user
    cursor.execute(
        "INSERT INTO users (email, password) VALUES (%s, %s)",
        (email, hashed_password)
    )
    db.commit()

    cursor.close()
    db.close()

    return {"message": "User registered successfully"}, 201


# Login User
def login_user(data):
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return {"message": "Email and password required"}, 400

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM users WHERE email=%s",
        (email,)
    )

    user = cursor.fetchone()

    if not user:
        return {"message": "Invalid credentials"}, 401

    # Check password securely
    if not check_password_hash(user["password"], password):
        return {"message": "Invalid credentials"}, 401

    # Generate JWT token
    access_token = create_access_token(identity=user["email"])

    cursor.close()
    db.close()

    return {
        "message": "Login successful",
        "access_token": access_token
    }, 200