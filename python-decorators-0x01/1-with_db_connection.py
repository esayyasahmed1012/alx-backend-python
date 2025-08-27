# import sqlite3
# import functools
# from datetime import datetime

# def with_db_connection(func):
#     """ your code goes here""" 
#     @functools.wraps(func)
#     def wrapper(*args, **kwargs):
#         conn = sqlite3.connect('users.db')
#         try:
#             result = func(conn, *args, **kwargs)
#         finally:
#             conn.close()
#         return result
#     return wrapper    
# @with_db_connection 
# def get_user_by_id(conn, user_id): 
#     cursor = conn.cursor() 
#     cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,)) 
#     return cursor.fetchone()

# if __name__=="__main__":
#     user=get_user_by_id(user_id=1)
#     print(user)

import sqlite3
import functools
from datetime import datetime

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

@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone() # Fetch the single row
user = get_user_by_id(user_id=1)
print(user)
