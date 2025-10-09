import sqlite3
from sqlite3 import Connection, Row
from datetime import datetime

DB_FILE = "mood_logger.db"  # SQLite database file

def get_connection() -> Connection:
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = Row  # allows dict-like access to rows
    return conn


def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS moods (
        mood_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        time TIMESTAMP NOT NULL,
        mood TEXT NOT NULL,
        sentiment TEXT NOT NULL
    )
    ''')
    conn.commit()
    cursor.close()
    conn.close()


def add_mood(user_id, time: datetime, mood, sentiment):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO moods (user_id, time, mood, sentiment) VALUES (?, ?, ?, ?)',
        (user_id, time, mood, sentiment)
    )
    conn.commit()
    cursor.close()
    conn.close()


def get_moods(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT mood_id, time, mood FROM moods WHERE user_id = ?', (user_id,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [dict(row) for row in rows]


def delete_mood_db(mood_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM moods WHERE mood_id = ?', (mood_id,))
    conn.commit()
    cursor.close()
    conn.close()


def get_mood_count(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM moods WHERE user_id = ?', (user_id,))
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count