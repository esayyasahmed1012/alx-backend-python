# 1-execute.py
import sqlite3

class ExecuteQuery:
    """
    A context manager for executing SQL queries with parameters.
    Manages database connection and query execution, returning results.
    """
    def __init__(self, db_name, query, params=()):
        """Initialize with database name, query, and optional parameters."""
        self.db_name = db_name
        self.query = query
        self.params = params
        self.conn = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        """Open connection, execute query, and return results."""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_value, traceback):
        """Close cursor and connection, committing or rolling back based on exceptions."""
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
    # Create a sample users table with age column for testing
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            email TEXT,
            age INTEGER
        )''')
        # Insert sample data
        cursor.executemany(
            "INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?, ?)",
            [
                ('1', 'John', 'Doe', 'john@example.com', 30),
                ('2', 'Jane', 'Smith', 'jane@example.com', 22),
                ('3', 'Bob', 'Johnson', 'bob@example.com', 27)
            ]
        )
        conn.commit()

    # Use the context manager to execute the query
    query = "SELECT * FROM users WHERE age > ?"
    with ExecuteQuery('users.db', query, (25,)) as results:
        print("Users with age > 25:", results)