import asyncio
import aiosqlite


async def async_fetch_users():
    async with aiosqlite.connect('users.db') as db:
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            for user in users:
                print(f"All Users: {user}" )
            return users
        


async def async_fetch_older_users():
    async with aiosqlite.connect('users.db') as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            users = await cursor.fetchall()
            for user in users:
                print(f"Older Users: {user}")
            return users

async def fetch_concurrently(): await asyncio.gather( async_fetch_older_users(), async_fetch_users())

asyncio.run(fetch_concurrently())