import sqlite3
import os

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "tasks.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "schema.sql")

conn = sqlite3.connect(DB_PATH)

with open(SCHEMA_PATH) as f:
    conn.executescript(f.read())

conn.commit()
conn.close()

print("\o/ Base tasks.db créée avec succès !")

