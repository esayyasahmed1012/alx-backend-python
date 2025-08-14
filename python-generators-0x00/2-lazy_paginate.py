import os
import mysql.connector
import csv
from dotenv import load_dotenv

seed=__import__("seed")
load_dotenv()

db_config={
    'host':os.getenv("DB_HOST"),
    'user':os.getenv("DB_USER"),
    'password':os.getenv("DB_PASSWORD"),
    'database':os.getenv("DB_NAME")
}

def paginate_users(page_size, offset):
    
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows
def lazy_paginate(page_size):
    offset=0
    while(True):
        page=paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset+=page_size
    
        
        