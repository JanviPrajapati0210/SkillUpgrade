import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Vp17092006",
        database="skillupgrade"
    )
