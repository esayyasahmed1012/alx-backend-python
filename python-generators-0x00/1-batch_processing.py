import mysql.connector
from contextlib import contextmanager
import os
from dotenv import load_dotenv

load_dotenv()
# ✅ Clean DB config (no 'port', no 'table')
DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
}

@contextmanager
def get_db_connection():
    conn = mysql.connector.connect(**DB_CONFIG)
    try:
        yield conn
    finally:
        conn.close()

def stream_users_in_batches(batch_size):
    with get_db_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) FROM user_data")
        total_users = cursor.fetchone()['COUNT(*)']
        
        for offset in range(0, total_users, batch_size):
            cursor.execute(f"SELECT * FROM user_data LIMIT {batch_size} OFFSET {offset}")
            batch = cursor.fetchall()
            yield batch

def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        print(f"Processing batch of {len(batch)} users")
        for user in batch:
            print(user)
