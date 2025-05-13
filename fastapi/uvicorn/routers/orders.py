from fastapi import APIRouter, HTTPException
from typing import List
from models import Order, Item
import logging
from datetime import datetime

router = APIRouter(
    prefix="/orders",
    tags=["orders"]
)

# In-memory database
orders_db = {}

@router.post("/", response_model=Order)
async def create_order(order: Order):
    orders_db[order.id] = order
    return order

@router.get("/{order_id}", response_model=Order)
async def get_order(order_id: int):
    return orders_db[order_id]

@router.get("/", response_model=List[Order])
async def list_orders():
    return orders_db.values()

@router.put("/{order_id}/status")
async def update_order_status(order_id: int, status: str):
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Order not found")
    orders_db[order_id].status = status
    return {"message": "Order status updated successfully"}

@router.post("/{order_id}/items")
async def add_item_to_order(order_id: int, item: Item):
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Order not found")
    orders_db[order_id].items.append(item)
    return {"message": "Item added to order successfully"}

@router.get("/user/{user_id}")
async def get_user_orders(user_id: int):
    user_orders = []
    for order in orders_db.values():
        if order.user_id == user_id:
            user_orders.append(order)
    return user_orders 