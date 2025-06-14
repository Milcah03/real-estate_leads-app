import os
import random
from datetime import datetime, timedelta
from faker import Faker
import psycopg2
from dotenv import load_dotenv

load_dotenv()
fake = Faker()

SOURCES = ['WhatsApp', 'Facebook', 'Website', 'Instagram', 'Referral']
STATUSES = ['New', 'Contacted', 'Converted', 'Lost']
AGENTS = ['Fatima', 'Ahmed', 'Sara', 'Mohammed', 'Lina']

conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
)
cur = conn.cursor()

for _ in range(200):
    name = fake.name()
    phone = fake.phone_number()
    source = random.choice(SOURCES)
    agent = random.choice(AGENTS)
    timestamp = fake.date_time_between(start_date='-30d', end_date='now')
    status = random.choices(STATUSES, weights=[0.5, 0.3, 0.15, 0.05])[0]
    response_time = random.randint(2, 120) 

    cur.execute("""
        INSERT INTO leads (name, phone, source, agent_name, timestamp, status, response_time)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (name, phone, source, agent, timestamp, status, response_time))

conn.commit()
cur.close()
conn.close()
print("✅ Inserted 200 leads")
