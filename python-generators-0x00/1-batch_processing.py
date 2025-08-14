import os
import mysql.connector
import csv
from dotenv import load_dotenv

load_dotenv()

db_config={
    'host':os.getenv("DB_HOST"),
    'user':os.getenv("DB_USER"),
    'password':os.getenv("DB_PASSWORD"),
    'database':os.getenv("DB_NAME")
}


def db_connect():
    return mysql.connector.connect(**db_config)
def stream_users_in_batches(batch_size):
    connection=db_connect()
    cursor=connection.cursor(dictionary=True)
    offset=0
    while(True):
        cursor.execute("SELECT * FROM user_data LIMIT %s OFFSET %s", (batch_size, offset))
        batch=cursor.fetchall()
        if not batch:
            break
        yield batch
        offset+=batch_size
def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        filtered_user=[user for user in batch if user['age']>25]
        for user in filtered_user:
            print(user)