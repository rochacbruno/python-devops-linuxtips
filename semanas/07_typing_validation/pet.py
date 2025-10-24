# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "httpx",
#     "pydantic",
# ]
# ///
import httpx

from typing import Literal, Optional
from pydantic import BaseModel, Field
from pydantic_core.core_schema import LiteralSchema

BASE_URL = "https://petstore.swagger.io/v2"


class PartialPet(BaseModel):
    name: str = Field(..., description="Name of the pet")
    status: Optional[Literal["available", "pending", "sold"]] = None


class Pet(PartialPet):
    id: int = Field(..., description="Pet ID")


def add_pet(pet: PartialPet) -> Pet:
    response = httpx.post(f"{BASE_URL}/pet", json=pet.model_dump())
    response.raise_for_status()

    return Pet.model_validate(response.json())


def get_pet(pet_id: int) -> Pet:
    response = httpx.get(f"{BASE_URL}/pet/{pet_id}")
    response.raise_for_status()

    return Pet.model_validate(response.json())


def main():
    new_pet = PartialPet(name="manda chuva", status="pending")
    result = add_pet(new_pet)
    print(f"REsult: {result}")

    fetched = get_pet(result.id)
    print(f"Fetched {fetched}")


if __name__ == "__main__":
    # TODO: Migrar para usar click ou argparser
    import sys

    if len(sys.argv) == 1:
        print("Invalid usage, pass `add` or `get`")
        exit(1)
    with open(0) as stdin:
        if sys.argv[1] == "add":
            new_pet = PartialPet.model_validate_json(stdin.read())
            result = add_pet(new_pet)
            print(f"{result.id}")

        if sys.argv[1] == "get":
            result = get_pet(int(stdin.read()))
            print(f"{result}")
