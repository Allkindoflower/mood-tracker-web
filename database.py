import sqlite3

def get_connection():
    conn = sqlite3.connect('moods.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS moods (
        mood_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        time TEXT NOT NULL,
        mood TEXT NOT NULL,
        sentiment TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

def add_mood(user_id, time, mood, sentiment):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO moods (user_id, time, mood, sentiment) VALUES (?, ?, ?, ?)', (user_id, time, mood, sentiment))
    conn.commit()
    conn.close()

def get_moods(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT mood_id, time, mood FROM moods WHERE user_id = ?', (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def delete_mood_db(mood_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM moods WHERE mood_id = ?', (mood_id,))
    conn.commit()
    conn.close()

def get_mood_count(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM moods WHERE user_id = ?', (user_id,))
    count = cursor.fetchone()[0]
    conn.close()
    return count
