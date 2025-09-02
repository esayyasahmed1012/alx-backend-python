import aiosqlite
import asyncio

async def async_fetch_users():
    async with aiosqlite.connect('user.db') as conn:
        cursor=await conn.cursor()
        await cursor.execute("SELECT * FROM users")
        all_users=await cursor.fetchall()
        await cursor.close()
        return all_users
async def async_fetch_older_users() :
    async with aiosqlite.connect("user.db") as conn:
        cursor=await conn.cursor()
        await cursor.execute("SELECT * FROM users where age > 40")
        old_users = await cursor.fetchall()
        await cursor.close()
        return old_users
    

async def concurent_fetch():
    all_users, old_users=await asyncio.gather(
        async_fetch_users(), async_fetch_older_users()
    )
    return all_users, old_users


all_users, old_users=asyncio.run(concurent_fetch())
print(f"all users: {all_users}, old users: {old_users}")