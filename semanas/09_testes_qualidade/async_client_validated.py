import asyncio
import httpx
from models import Product 

prods = list(range(1, 2))




async def get_product(client: httpx.AsyncClient, product: int):
    response = await client.get(f"https://fakestoreapi.com/products/{product}")
    if product % 2 == 0:
        await asyncio.sleep(1)
    return product, response.json()


async def main():
    async with httpx.AsyncClient() as client:
        tasks = [get_product(client, prod) for prod in prods]
        for coro in asyncio.as_completed(tasks):
            prod, resp = await coro
            print(resp)
            new = Product.model_validate(resp)
            print(new)


if __name__ == "__main__":
    asyncio.run(main())
