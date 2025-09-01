import time
import sqlite3 
import functools

#### paste your with_db_decorator here
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
    @functools.wraps(func)
    def wrapper(conn,*args, **kwargs):
        try:
            result=func(conn, *args, **kwargs)
            conn.commit()
        except Exception as e:
            conn.rollback()
            print("can't update teh table due to error")
        return result

    return wrapper
    pass
@with_db_connection
@retry_on_failure(retries=3, delay=1)

def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)