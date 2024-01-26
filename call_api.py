import asyncio
from aiohttp import ClientSession


async def call_api(url: str):
    async with ClientSession() as session:
        async with session.get(url) as response:
            response = await response.text()
            print(response)


async def main():
    base_url = "http://localhost:8000"
    endpoints = ["slow-query", "slow-external-api", "hello-world", "error"]
    async with asyncio.TaskGroup() as group:
        for endpoint in endpoints:
            url = f"{base_url}/{endpoint}"
            for i in range(20):
                group.create_task(call_api(url))

asyncio.run(main())