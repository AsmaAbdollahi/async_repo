import aiohttp
import asyncio

class Fetcher:
    def __init__(self, urls):
        self.urls = urls

    async def fetch(self, session, url):
        try:
            async with session.get(url) as response:
                return url, await response.text()
        except Exception as e:
            return url, f"Error: {e}"

    async def run(self):
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch(session, url) for url in self.urls]
            return await asyncio.gather(*tasks)
