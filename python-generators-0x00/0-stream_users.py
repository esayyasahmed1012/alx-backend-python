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
    connection=mysql.connector.connect(**db_config)
    return connection
def stream_users():
    connection=db_connect()
    cursor=connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM user_data")
        for row in cursor:
            yield row
    except mysql.connector.Error as e:
        print(f"mysql error {e}")
    finally:
        cursor.close()
        connection.close()
    
        
from itertools import islice
for user in islice(stream_users(), 6):
    print(user)