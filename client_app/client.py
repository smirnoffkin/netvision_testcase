import asyncio
import random
import string
import uuid
from datetime import datetime as dt

import aiohttp

STRING_MAX_LENGHT = 16
COUNT_REQUESTS_PER_SECOND = 100

async def get_random_post_data() -> dict:
    uuid_data = uuid.uuid4()
    text = ''.join(random.choice(string.ascii_letters) for _ in range(STRING_MAX_LENGHT))

    return {"uuid": uuid_data.hex, "text": text}


async def make_request():
    post_data = await get_random_post_data()
    async with aiohttp.ClientSession("http://localhost:8080") as session:
        async with session.post("/new", json=post_data) as resp:
            print(resp.status)
            print(await resp.text())


async def main():
    async with asyncio.TaskGroup() as group:
        for _ in range(COUNT_REQUESTS_PER_SECOND):
            group.create_task(make_request())
            await asyncio.sleep(0.1)


if __name__ == "__main__":
    asyncio.run(main())