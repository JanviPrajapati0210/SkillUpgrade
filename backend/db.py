import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# ------------------ LOAD ENV VARIABLES ------------------

load_dotenv()

# ------------------ DB CONNECTION FUNCTION ------------------

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=os.getenv("DB_PORT", 3306),
            autocommit=False
        )

        if connection.is_connected():
            return connection

    except Error as e:
        print("Database connection error:", e)
        return None
