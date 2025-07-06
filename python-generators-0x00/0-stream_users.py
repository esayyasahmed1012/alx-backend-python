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

# Validate all required environment variables are set
required_env_vars = {'DB_HOST', 'DB_USER', 'DB_PASSWORD', 'DB_NAME'}
missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars:
    raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

@contextmanager
def connect_db():
    """Connects to the MySQL database server."""
    connection = mysql.connector.connect(**DB_CONFIG)
    try:
        yield connection
    finally:
        connection.close()

def stream_users():
    """Generator that streams rows from the user_data table one by one as dictionaries.
    
    Yields:
        dict: A dictionary containing user_id, name, email, and age for each row.
    """
    with connect_db() as connection:
        cursor = connection.cursor(dictionary=True)  # Use dictionary cursor for dict output
        cursor.execute("SELECT user_id, name, email, age FROM user_data")
        row = cursor.fetchone()
        while row is not None:
            yield row
            row = cursor.fetchone()
        cursor.close()

if __name__ == "__main__":
    # Example usage for testing
    for user in stream_users():
        print(user)