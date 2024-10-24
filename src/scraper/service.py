import aiohttp
from bs4 import BeautifulSoup
from models import Product
from src.databse import get_session


async def fetch_page(session, url):
    async with session.get(url) as response:
        return await response.text()


async def parse_page(html):
    soup = BeautifulSoup(html, 'lxml')
    products = []
    for item in soup.select('.product-item'):
        name = item.select_one().text
        price = float(item.select_one().text)
        category = item.select_one().text
        image_url = item.select_one()['src']
        description = item.select_one().text
        products.append({"name": name, "price": price, "category": category, "image_url": image_url, "description": description})
    return products


async def scrape_products(url):
    async with aiohttp.ClientSession() as session:
        html = await fetch_page(session, url)
        products = await parse_page(html)
        async with get_session() as db_session:
            for product_data in products:
                product = Product(**product_data)
                db_session.add(product)
            await db_session.commit()
