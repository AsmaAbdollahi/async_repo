import aiofiles

class Writer:
    def __init__(self, filename):
        self.filename = filename

    async def write(self, results):

        async with aiofiles.open(self.filename, "w", encoding="utf-8") as f:
            for url, content in results:

                await f.write(f"===== {url} =====\n")
                await f.write(content[:500])  
                await f.write("\n\n")
