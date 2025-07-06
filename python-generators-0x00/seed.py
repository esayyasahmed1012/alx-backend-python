import mysql.connector
import csv
import uuid
import os
from dotenv import load_dotenv
from contextlib import contextmanager

# Load environment variables from .env file
load_dotenv()

# Database connection configuration from environment variables only
DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

# Validate all required environment variables are set
required_env_vars = {'DB_HOST', 'DB_USER', 'DB_PASSWORD', 'DB_NAME'}
missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars:
    raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

@contextmanager
def connect_db():
    """Connects to the MySQL database server."""
    connection = mysql.connector.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password']
    )
    try:
        yield connection
    finally:
        connection.close()

def create_database(connection):
    """Creates the database if it does not exist."""
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS " + DB_CONFIG['database'])
    cursor.close()

def connect_to_prodev():
    """Connects to the specified database in MySQL."""
    return mysql.connector.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        database=DB_CONFIG['database']
    )

def create_table(connection):
    """Creates a table user_data if it does not exist with the required fields."""
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(5,2) NOT NULL,
            INDEX (user_id)
        )
    """)
    print("Table user_data created successfully")
    cursor.close()

def insert_data(connection, csv_file):
    """Inserts data into the database if it does not exist."""
    cursor = connection.cursor()
    insert_query = """
        INSERT IGNORE INTO user_data (user_id, name, email, age)
        VALUES (%s, %s, %s, %s)
    """
    csv_data = []
    try:
        with open(csv_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                csv_data.append((
                    row['user_id'],
                    row['name'],
                    row['email'],
                    float(row['age'])
                ))
    except FileNotFoundError:
        print("user_data.csv not found. No data inserted.")
        return

    if csv_data:
        cursor.executemany(insert_query, csv_data)
        connection.commit()
        print(f"Inserted {len(csv_data)} rows into table.")
    cursor.close()

def stream_rows():
    """Generator that streams rows from the user_data table one by one."""
    with connect_to_prodev() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user_data")
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            yield row
        cursor.close()

if __name__ == "__main__":
    # Example usage of the generator (for testing)
    for row in stream_rows():
        print(row)