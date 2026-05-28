import sqlite3

# Connect database
conn = sqlite3.connect("study_history.db")

# Cursor
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS history (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    question TEXT,

    answer TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()

# Save function
def save_history(question, answer):

    conn = sqlite3.connect("study_history.db")

    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO history(question, answer)

    VALUES (?, ?)

    """, (question, answer))

    conn.commit()

    conn.close()

# View history
def get_history():

    conn = sqlite3.connect("study_history.db")

    cursor = conn.cursor()

    cursor.execute("""

    SELECT * FROM history
    ORDER BY id DESC

    """)

    data = cursor.fetchall()

    conn.close()

    return data