# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "fastapi",
#     "pydantic",
# ]
# ///

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List

app = FastAPI()

class User(BaseModel):
    name: str
    email: str
    role: str = "user"

class UserResponse(User):
    id: int

users: Dict[int, UserResponse] = {}  # DATABASE SIMULADA

@app.get("/users", response_model=List[UserResponse])
async def get_users():
    return list(users.values())

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return users[user_id]

@app.post("/users", response_model=UserResponse, status_code=201)
async def create_user(user: User):
    user_response = UserResponse(id=next_id, **user.dict())
    users[next_id] = user_response
    next_id += 1
    return user_response

@app.delete("/users/{user_id}", status_code=204)
async def delete_user(user_id: int):
    users.pop(user_id, None)
    return None