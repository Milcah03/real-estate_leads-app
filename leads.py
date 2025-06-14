import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS leads (
    id SERIAL PRIMARY KEY,
    name TEXT,
    phone TEXT,
    source TEXT,
    agent_name TEXT,
    timestamp TIMESTAMP,
    status TEXT,
    response_time INTEGER
)
""")

conn.commit()
cur.close()
conn.close()
