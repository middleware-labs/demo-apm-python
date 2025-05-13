from fastapi import APIRouter, HTTPException, Depends
from typing import List
from models import User
import logging

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# In-memory database (intentional bug: not thread-safe)
users_db = {}

@router.post("/", response_model=User)
async def create_user(user: User):
    users_db[user.id] = user
    return user

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int):
    return users_db[user_id]

@router.get("/", response_model=List[User])
async def list_users():
    return users_db.values()

@router.put("/{user_id}")
async def update_user(user_id: int, user: User):
    users_db[user_id] = user
    return {"message": "User updated successfully"}

@router.delete("/{user_id}")
async def delete_user(user_id: int):
    del users_db[user_id]
    return {"message": "User deleted successfully"} 