# 0-databaseconnection.py
import sqlite3

class DatabaseConnection:
    """
    A context manager for handling SQLite3 database connections.
    Automatically opens and closes connections using __enter__ and __exit__.
    """
    def __init__(self, db_name):
        """Initialize with the database name."""
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def __enter__(self):
        """Open the database connection and return the cursor."""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        """Close the cursor and connection, committing or rolling back based on exceptions."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            if exc_type is None:  # No exception, commit changes
                self.conn.commit()
            else:  # Exception occurred, rollback
                self.conn.rollback()
            self.conn.close()

# Test the context manager
if __name__ == "__main__":
    # Create a sample users table for testing
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            email TEXT
        )''')
        cursor.execute("INSERT OR IGNORE INTO users VALUES ('1', 'John', 'Doe', 'john@example.com')")
        conn.commit()

    # Use the context manager to execute SELECT * FROM users
    with DatabaseConnection('users.db') as cursor:
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        print("Fetched users:", results)