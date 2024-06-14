import sqlite3

# Connect to SQLite database (will create if not exists)
conn = sqlite3.connect('form_data.db')
cursor = conn.cursor()

# Create a table to store form data
cursor.execute('''
    CREATE TABLE IF NOT EXISTS FormData (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        college TEXT NOT NULL,
        pref1 TEXT,
        pref2 TEXT,
        pref3 TEXT
    )
''')

conn.commit()
