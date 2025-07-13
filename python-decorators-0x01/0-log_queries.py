import sqlite3
import functools
import logging
import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('database_queries.log'),  # Log to a file
        logging.StreamHandler()  # Also log to console
    ]
)

def log_queries(func):
    """
    Decorator to log SQL queries executed by a function.
    Logs the query with a timestamp before execution.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Get the query from the arguments (assuming query is the first argument)
        query = args[0] if args else kwargs.get('query', 'Unknown query')
        logging.info(f"Executing SQL query: {query}")
        # Execute the original function
        result = func(*args, **kwargs)
        return result
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Example usage
if __name__ == "__main__":
    # Create a sample users table for testing
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        email TEXT
    )''')
    cursor.execute("INSERT OR IGNORE INTO users VALUES ('1', 'John', 'Doe', 'john@example.com')")
    conn.commit()
    conn.close()

    # Fetch users while logging the query
    users = fetch_all_users(query="SELECT * FROM users")
    print("Fetched users:", users)