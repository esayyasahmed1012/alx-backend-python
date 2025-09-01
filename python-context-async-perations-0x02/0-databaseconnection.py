
import sqlite3
class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name=db_name
        self.conn=None

    def __enter__(self):
        self.conn=sqlite3.connect(self.db_name)
        return self.conn
    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            self.conn.close()
            print("connection is closed")

with DatabaseConnection('user.db') as conn:
    cursor=conn.cursor()
    cursor.execute("Select * from Users") 
    result = cursor.fetchall()
    for row in result:
        print(row)
