import sqlite3

class ExecuteQuery:
    def __init__(self, db_name, query, params=()):
        self.db_name=db_name
        self.query=query
        self.params=params
        self.conn=None
        self.cursor=None
        self.result=None

    def __enter__(self):
        self.conn=sqlite3.connect(self.db_name)
        self.cursor=self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        self.result=self.cursor.fetchall()
        return self.result
    def __exit__(self, exc_type, exc_value, traceback):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            if exc_type is None:
                self.conn.close()
            else:
                self.conn.rollback()
query = "SELECT * FROM users WHERE age > ?"
with ExecuteQuery('user.db', query, (25,)) as results:
    print("Users with age > 25:", results)

            
        
        