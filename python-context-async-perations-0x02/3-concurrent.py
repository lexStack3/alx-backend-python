#!/usr/bin/python3
"""Runs multiple database queries concurrently using
<asyncio.gather>.
"""
import asyncio
import aiosqlite


async def async_fetch_users():
    """Fetches all users from the users sqlite database."""
    async with aiosqlite.connect('users.db') as conn:
        async with conn.execute("SELECT * FROM users") as cursor:
            return await cursor.fetchall()


async def async_fetch_older_users():
    """Fetches all users from the users.db sqlite database older
    than the age 40.
    """
    async with aiosqlite.connect('users.db') as conn:
        async with conn.execute(
                "SELECT * FROM users WHERE age > ?", (40,)
                ) as cursor:
            return await cursor.fetchall()


async def fetch_concurrently():
    """Executes both queries concurrently."""
    task1 = asyncio.create_task(async_fetch_users())
    task2 = asyncio.create_task(async_fetch_older_users())

    results = await asyncio.gather(task1, task2)

    for users in results:
        for user in users:
            print(user)
        print("{}".format('-' * 50 if users is results[:-1][0] else ''))


if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
