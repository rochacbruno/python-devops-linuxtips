# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "httpx",
#     "pytest",
# ]
# ///
import json
import httpx


def test_contract():
    current_spec = httpx.get("https://fakestoreapi.com/docs-data")
    with open("spec.json", "r") as f:
        old_spec = json.load(f)

    assert current_spec == old_spec


def test_product_api():
    response = httpx.get("https://fakestoreapi.com/products/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1
