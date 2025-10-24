# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "pydantic[email]",
# ]
# ///
from pydantic import (
    BaseModel,
    EmailStr,
    field_validator,
)

import json

with open("data.json") as f:
    data = json.load(f)


# Model / Schema
class User(BaseModel):
    name: str
    age: int
    email: EmailStr
    height: float
    active: bool

    @field_validator("email")
    def validate_email(cls, v):
        if v.endswith("gmail.com"):
            raise ValueError("Gmail not accepted")

    @field_validator("height")
    def validate_height(cls, v):
        if not (0.5 <= v <= 2.5):
            raise ValueError("Height must be between 0.5-2.5")


user = User(**data)
