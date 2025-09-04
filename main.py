import asyncio
import os
from dotenv import load_dotenv
from fetch import Fetcher
from writer import Writer

async def main():
    #  use defined urls and file for saving the content
    # Load env file
    load_dotenv(".eve.example")

    urls = [os.getenv("URL_1"), os.getenv("URL_2"), os.getenv("URL_3")]
    output_file = os.getenv("OUTPUT_FILE")

    fetcher = Fetcher(urls)
    results = await fetcher.run()

    writer = Writer(output_file)
    await writer.write(results)

if __name__ == "__main__":
    asyncio.run(main())
