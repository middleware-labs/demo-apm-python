from fastapi import APIRouter, HTTPException, Depends
from typing import List
from models import User
import logging
import time
from datetime import datetime

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# In-memory database (intentional bug: not thread-safe)
users_db = {}

def initialize_dummy_users():
    dummy_users = [
        User(
            id=1,
            username="john_doe",
            email="john@example.com",
            is_active=True,
            created_at=datetime.now()
        ),
        User(
            id=2,
            username="jane_smith",
            email="jane@example.com",
            is_active=True,
            created_at=datetime.now()
        ),
        User(
            id=3,
            username="bob_wilson",
            email="bob@example.com",
            is_active=False,
            created_at=datetime.now()
        )
    ]
    for user in dummy_users:
        users_db[user.id] = user

# Initialize dummy data
initialize_dummy_users()

@router.post("/", response_model=User)
async def create_user(user: User):
    # Bug 1: Type error - trying to use string as integer
    user.id = str(user.id)  # This will cause a type error
    users_db[user.id] = user
    return user

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int):
    # Bug 2: Incorrect error handling
    try:
        return users_db[user_id]
    except:
        return {"error": "User not found"}  # Should use HTTPException

@router.get("/", response_model=List[User])
async def list_users():
    # Bug 3: Infinite recursion
    return list_users()  # This will cause stack overflow

@router.put("/{user_id}")
async def update_user(user_id: int, user: User):
    # Bug 4: Race condition
    time.sleep(2)  # Simulating slow operation
    users_db[user_id] = user
    return {"message": "User updated successfully"}

@router.delete("/{user_id}")
async def delete_user(user_id: int):
    # Bug 5: Incorrect dictionary access
    del users_db[str(user_id)]  # Type mismatch with integer key
    return {"message": "User deleted successfully"}

# Bug 6: Memory leak in a utility function
def get_user_details(user_id: int):
    details = []
    while True:
        details.append({"id": user_id, "timestamp": time.time()})
    return details 