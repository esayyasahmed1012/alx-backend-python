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

def db_connect():
    return mysql.connector.connect(**db_config)
def stream_user_ages():
    conncetion=db_connect()
    cursor=conncetion.cursor()
    cursor.execute("SELECT age FROM user_data")
    for row in cursor:
        yield row[0]


def calculate_average_age():
    count=0
    total=0
    for age in stream_user_ages():
        count+=1
        total+=age
    avg=total/count
    print(f"the average age is {avg}")


calculate_average_age()