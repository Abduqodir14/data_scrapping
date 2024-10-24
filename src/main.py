import asyncio
from scraper.service import scrape_products

urls = ["https://mediapark.uz", "https://texnomart.uz"]


async def main():
    tasks = [scrape_products(url) for url in urls]
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())
