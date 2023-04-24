from gpt import generate_html
import asyncio
import json

pages = {}


async def main():
    with open('pages.json', 'w') as f:
        json.dump(pages, f)

asyncio.run(main())
