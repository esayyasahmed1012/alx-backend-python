import sqlite3

class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name=db_name
        self.connection=None

    def __enter__(self):
        self.connection=sqlite3.connect(self.db_name)
        return self.connection
    
    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection:
            self.connection.close()
            print("Database Conection CLosed.")
def setup_users_table(db_name):
    with DatabaseConnection(db_name) as conn:
        cursor=conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE
                )
        """)
        sample_users=[
            ('Alice', 'alice@gmail.com'),
            ('bob', 'bob@example.com'),
            ('Charlie', 'chalie@example.com')
        ]        
        cursor.executemany('INSERT OR IGNORE INTO users (name,email) VALUES (?, ?)', sample_users)
        conn.commit()
        print("Users Table created and sample data insered.")

def test_users_table(db_name):
    with DatabaseConnection(db_name) as conn:
        cursor=conn.cursor()
        cursor.execute("SELECT * FROM users")
        results=cursor.fetchall()
        for user in results:
            print(user)
if __name__=="__main__":
    db_name='test.db'
    setup_users_table(db_name)
    test_users_table(db_name)