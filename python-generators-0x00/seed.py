import mysql.connector
import os
from dotenv import load_dotenv
import csv
import uuid

load_dotenv()

db_config={
    'host':os.getenv("DB_HOST"),
    'user':os.getenv("DB_USER"),
    'password':os.getenv("DB_PASSWORD"),
    'database':os.getenv("DB_NAME")
}

def connect_db():
    connection=mysql.connector.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password']
    )
    return connection
def create_database(connection):
    cursor=connection.cursor()
    db_name=db_config['database']
    try:
        query=f"CREATE DATABASE IF NOT EXISTS {db_name}"
        cursor.execute(query)
        connection.commit()
    except mysql.connector.Error as e:
        print(e)
    finally:
        cursor.close()

def connect_to_prodev():
    connection=mysql.connector.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database']
    )
    return connection
def create_table(connection):
    cursor=connection.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS user_data(
               user_id VARCHAR(36) primary key,
               name VARCHAR(200) NOT NULL, 
               email VARCHAR(200) NOT NULL,
               age  DECIMAL(3,0) NOT NULL
             );
        """
    )
    connection.commit()
    cursor.close()
def insert_data(connection, data):
    cursor=connection.cursor()
    query="""
        INSERT IGNORE INTO user_data(user_id, name, email, age) values(%s, %s, %s, %s)
     """
    rows=[]
    with open(data, 'r') as f:
        data=csv.DictReader(f)
        rows=[]
        for row in data:
            user_id=str(uuid.uuid4())
            name=row['name']
            email=row['email']
            age=row['age']
            rows.append((user_id, name, email, age))
    if rows:
        cursor.executemany(query, rows)
        connection.commit()
    cursor.close()
   