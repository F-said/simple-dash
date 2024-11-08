"""
A file to tear down the db
"""

import sqlite3

conn = sqlite3.connect("db/responses.db")
c = conn.cursor()

c.execute('''DROP TABLE responses;''')

conn.commit()
