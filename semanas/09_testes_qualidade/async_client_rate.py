import asyncio
import httpx

prods = list(range(1, 11))  # demo with 20 products
MAX_CONCURRENT = 2  # limit concurrency

sem = asyncio.Semaphore(MAX_CONCURRENT)


async def get_product(client: httpx.AsyncClient, product: int):
    async with sem:  # limit concurrency
        response = await client.get(f"https://fakestoreapi.com/products/{product}")
        if product % 2 == 0:
            await asyncio.sleep(1)
        return product, response.json()


async def main():
    async with httpx.AsyncClient() as client:
        tasks = [get_product(client, prod) for prod in prods]
        for coro in asyncio.as_completed(tasks):
            prod, resp = await coro
            print(f"{prod}: {resp['title']}\n")


if __name__ == "__main__":
    asyncio.run(main())
