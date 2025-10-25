import httpx
import time

prods = list(range(1, 11))


def get_product(product: int):
    response = httpx.get(f"https://fakestoreapi.com/products/{product}")
    if product % 2 == 0:
        time.sleep(1)
    return response.json()


def main():
    for prod in prods:
        resp = get_product(prod)
        print(prod, resp["title"], end="\n\n")


if __name__ == "__main__":
    main()
