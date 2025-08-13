from dotenv import load_dotenv
import os
import psycopg2
from psycopg2.extras import RealDictCursor

load_dotenv()
def get_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    return conn


def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS moods (
        mood_id SERIAL PRIMARY KEY,
        user_id TEXT NOT NULL,
        time TIMESTAMP NOT NULL,
        mood TEXT NOT NULL,
        sentiment TEXT NOT NULL
    )
    ''')
    conn.commit()
    cursor.close()
    conn.close()


def add_mood(user_id, time, mood, sentiment):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO moods (user_id, time, mood, sentiment) VALUES (%s, %s, %s, %s)',
        (user_id, time, mood, sentiment)
    )
    conn.commit()
    cursor.close()
    conn.close()


def get_moods(user_id):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('SELECT mood_id, time, mood FROM moods WHERE user_id = %s', (user_id,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def delete_mood_db(mood_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM moods WHERE mood_id = %s', (mood_id,))
    conn.commit()
    cursor.close()
    conn.close()


def get_mood_count(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM moods WHERE user_id = %s', (user_id,))
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count

