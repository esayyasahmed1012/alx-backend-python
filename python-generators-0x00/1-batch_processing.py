# 1-batch_processing.py

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

def stream_users_in_batches(batch_size):
    """
    Generator function to fetch users from the database in batches.
    
    Args:
        batch_size (int): Number of users to fetch per batch.
    
    Yields:
        list: A batch of user dictionaries.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor(dictionary=True)  # Fetch as dictionaries
        cursor.execute("SELECT COUNT(*) FROM user_data")  # Changed from 'users' to 'user_data'
        total_users = cursor.fetchone()['COUNT(*)']
        offset = 0
        while offset < total_users:  # Loop 1: Iterate over batches
            cursor.execute(
                "SELECT user_id, name, email, age FROM user_data LIMIT %s OFFSET %s",  # Changed to 'user_data'
                (batch_size, offset)
            )
            batch = cursor.fetchall()
            yield batch
            offset += batch_size
        cursor.close()

def batch_processing(batch_size):
    """
    Generator function to process each batch of users and filter those over the age of 25.
    
    Args:
        batch_size (int): Number of users to process per batch.
    
    Yields:
        dict: User details for users over 25.
    """
    user_stream = stream_users_in_batches(batch_size)
    for batch in user_stream:  # Loop 2: Iterate over yielded batches
        for user in batch:  # Loop 3: Iterate over users in batch
            if user['age'] > 25:
                yield user  # Return filtered user instead of print

if __name__ == "__main__":
    for user in batch_processing(50):
        print(user)