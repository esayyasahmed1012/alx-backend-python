# 3-average_age.py

import mysql.connector
import os
from dotenv import load_dotenv
from contextlib import contextmanager

# Load environment variables from .env file
load_dotenv()

# Database connection configuration from environment variables
DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

@contextmanager
def get_db_connection():
    """Context manager for database connection."""
    conn = mysql.connector.connect(**DB_CONFIG)
    try:
        yield conn
    finally:
        conn.close()

def stream_user_ages():
    """
    Generator function to yield user ages one by one from the database.
    
    Yields:
        int: Age of each user.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT age FROM user_data")
        for row in cursor:  # Loop 1: Iterate over database rows
            yield row[0]  # Yield the age (first column)
        cursor.close()

def calculate_average_age():
    """
    Calculate the average age using the generator, without loading all data into memory.
    
    Prints:
        str: Average age of users.
    """
    total_age = 0
    count = 0
    for age in stream_user_ages():  # Loop 2: Iterate over yielded ages
        total_age += age
        count += 1
    average_age = total_age / count if count > 0 else 0
    print(f"Average age of users: {average_age}")

if __name__ == "__main__":
    calculate_average_age()