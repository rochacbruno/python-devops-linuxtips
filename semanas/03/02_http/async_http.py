# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "aiohttp",
# ]
# ///

import asyncio
import aiohttp 

async def fetch_user(session, user_id):
    url = (
            'https://jsonplaceholder.typicode.com/users/'
            f'{user_id}'
    )
    async with session.get(url) as response:
        await asyncio.sleep(1)  # Simular latência
        print(f"Fetched user {user_id}")
        return await response.json()

async def fetch_all_users():
    async with aiohttp.ClientSession() as session:
        # Buscar 10 usuários em paralelo
        tasks = [
            fetch_user(session, i) 
            for i in range(1, 11)
        ]
        users = await asyncio.gather(*tasks) 
        print("\nUsuários:")
        for user in users:
            print(f"- {user['name']} ({user['email']})")

asyncio.run(fetch_all_users())