import sqlite3 
import functools
import time
"""your code goes here"""

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper

def retry_on_failure(retries=3, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt=0
            while (attempt<retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"trying attempt {attempt+1} due to the error happend {e}")
                    attempt+=1
                    time.sleep(delay)
            raise Exception("attempt failed")
        return wrapper
    return decorator
@with_db_connection 
@retry_on_failure(retries=3, delay=1)

def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)

