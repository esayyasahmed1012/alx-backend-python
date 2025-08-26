import sqlite3

class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name=db_name
        self.connection=None

    def __enter__(self):
        self.connection=sqlite3.connect(self.db_name)
        return self.connection
    def __exit__(self):
        if self.connection:
            self.connection.close()
            print("connection closed")        
with DatabaseConnection("sqlite.db") as conn:
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM users")