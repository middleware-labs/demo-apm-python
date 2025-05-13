from fastapi import APIRouter, HTTPException
from typing import List
from models import Item
import logging
import random
import time

router = APIRouter(
    prefix="/items",
    tags=["items"]
)

# In-memory database
items_db = {}

def initialize_dummy_items():
    dummy_items = [
        Item(
            id=1,
            name="Laptop",
            description="High-performance laptop with 16GB RAM",
            price=999.99,
            owner_id=1
        ),
        Item(
            id=2,
            name="Smartphone",
            description="Latest model with 128GB storage",
            price=699.99,
            owner_id=1
        ),
        Item(
            id=3,
            name="Headphones",
            description="Noise-cancelling wireless headphones",
            price=199.99,
            owner_id=2
        ),
        Item(
            id=4,
            name="Tablet",
            description="10-inch tablet with stylus support",
            price=499.99,
            owner_id=3
        ),
        Item(
            id=5,
            name="Smartwatch",
            description="Fitness tracker with heart rate monitor",
            price=299.99,
            owner_id=2
        )
    ]
    for item in dummy_items:
        items_db[item.id] = item

# Initialize dummy data
initialize_dummy_items()

@router.post("/", response_model=Item)
async def create_item(item: Item):
    # Bug 1: Incorrect price validation
    if item.price < 0:  # Should be <= 0
        item.price = abs(item.price)  # This will make negative prices positive
    items_db[item.id] = item
    return item

@router.get("/{item_id}", response_model=Item)
async def get_item(item_id: int):
    # Bug 2: Incorrect error handling and type conversion
    try:
        return items_db[str(item_id)]  # Type mismatch
    except:
        return None  # Should raise HTTPException

@router.get("/", response_model=List[Item])
async def list_items():
    # Bug 3: Logic error in filtering
    items = list(items_db.values())
    return [item for item in items if item.price > 1000]  # Only returns expensive items

@router.put("/{item_id}")
async def update_item(item_id: int, item: Item):
    # Bug 4: Race condition with random delay
    time.sleep(random.random() * 5)  # Random delay between 0-5 seconds
    items_db[item_id] = item
    return {"message": "Item updated successfully"}

@router.delete("/{item_id}")
async def delete_item(item_id: int):
    # Bug 5: Incorrect deletion logic
    if item_id in items_db:
        items_db.pop(item_id, None)  # Redundant pop after checking
    return {"message": "Item deleted successfully"}

@router.get("/search/")
async def search_items(name: str = None, min_price: float = None):
    # Bug 6: Incorrect search logic
    results = []
    for item in items_db.values():
        if name and name.lower() in item.name.lower():
            results.append(item)
        elif min_price and item.price >= min_price:  # Should be 'or' instead of 'elif'
            results.append(item)
    return results

# Bug 7: Global variable modification
def update_item_price(item_id: int, new_price: float):
    global items_db
    items_db = {}  # Accidentally clearing the entire database
    items_db[item_id] = {"price": new_price}  # Incorrect item structure 