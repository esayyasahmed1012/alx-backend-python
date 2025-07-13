# 3-concurrent.py
import aiosqlite
import asyncio

async def async_fetch_users():
    """
    Asynchronously fetch all users from the users table.
    """
    async with aiosqlite.connect('users.db') as conn:
        cursor = await conn.execute("SELECT * FROM users")
        results = await cursor.fetchall()
        await cursor.close()
        return results

async def async_fetch_older_users():
    """
    Asynchronously fetch users older than 40 from the users table.
    """
    async with aiosqlite.connect('users.db') as conn:
        cursor = await conn.execute("SELECT * FROM users WHERE age > ?", (40,))
        results = await cursor.fetchall()
        await cursor.close()
        return results

async def fetch_concurrently():
    """
    Execute async_fetch_users and async_fetch_older_users concurrently using asyncio.gather.
    """
    # Run both queries concurrently
    all_users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    return all_users, older_users

# Test the concurrent queries
if __name__ == "__main__":
    # Create a sample users table with age column for testing
    with aiosqlite.connect('users.db') as conn:
        cursor = conn.execute('''CREATE TABLE IF NOT EXISTS users (
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
                ('1', 'John', 'Doe', 'john@example.com', 45),
                ('2', 'Jane', 'Smith', 'jane@example.com', 22),
                ('3', 'Bob', 'Johnson', 'bob@example.com', 50),
                ('4', 'Alice', 'Brown', 'alice@example.com', 35)
            ]
        )
        conn.commit()

    # Run concurrent queries
    all_users, older_users = asyncio.run(fetch_concurrently())
    print("All users:", all_users)
    print("Users older than 40:", older_users)