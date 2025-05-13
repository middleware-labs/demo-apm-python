from fastapi import APIRouter, HTTPException
from typing import List
from models import Item
import logging

router = APIRouter(
    prefix="/items",
    tags=["items"]
)

# In-memory database
items_db = {}

@router.post("/", response_model=Item)
async def create_item(item: Item):
    items_db[item.id] = item
    return item

@router.get("/{item_id}", response_model=Item)
async def get_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]

@router.get("/", response_model=List[Item])
async def list_items():
    return items_db.values()

@router.put("/{item_id}")
async def update_item(item_id: int, item: Item):
    items_db[item_id] = item
    return {"message": "Item updated successfully"}

@router.delete("/{item_id}")
async def delete_item(item_id: int):
    del items_db[item_id]
    return {"message": "Item deleted successfully"}

@router.get("/search/")
async def search_items(name: str = None, min_price: float = None):
    results = []
    for item in items_db.values():
        if name and name.lower() in item.name.lower():
            results.append(item)
        if min_price and item.price >= min_price:
            results.append(item)
    return results 