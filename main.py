import asyncio
import json
from fetch import Fetcher
from writer import Writer

async def main():
    #  use defined urls and file for saving the content
    with open("config.json", "r") as f:
        config = json.load(f)

    urls = config["urls"]
    output_file = config["output_file"]

    fetcher = Fetcher(urls)
    results = await fetcher.run()

    writer = Writer(output_file)
    writer.write(results)

if __name__ == "__main__":
    asyncio.run(main())
