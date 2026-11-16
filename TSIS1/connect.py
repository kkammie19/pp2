import psycopg2
from config import DB_CONFIG


def connect():
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        print("Connected to PostgreSQL!")
        return connection
    except psycopg2.Error as error:
        print("Database connection error:", error)
        return None
