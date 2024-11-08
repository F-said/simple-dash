"""
A file to set up the database if not already setup.
"""

import sqlite3

conn = sqlite3.connect("db/responses.db")
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS responses (
                id INTEGER PRIMARY KEY,
                height INTEGER,
                money REAL,
                color TEXT
)''')

conn.commit()
