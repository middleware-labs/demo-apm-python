from fastapi import APIRouter, HTTPException
from typing import List
from models import Order, Item
import logging
from datetime import datetime
import random

router = APIRouter(
    prefix="/orders",
    tags=["orders"]
)

# In-memory database
orders_db = {}

def initialize_dummy_orders():
    # First, create some items for the orders
    items = [
        Item(id=1, name="Laptop", price=999.99, owner_id=1),
        Item(id=2, name="Smartphone", price=699.99, owner_id=1),
        Item(id=3, name="Headphones", price=199.99, owner_id=2)
    ]
    
    dummy_orders = [
        Order(
            id=1,
            user_id=1,
            items=[items[0], items[1]],  # Laptop and Smartphone
            total_amount=1699.98,
            status="completed"
        ),
        Order(
            id=2,
            user_id=2,
            items=[items[2]],  # Headphones
            total_amount=199.99,
            status="processing"
        ),
        Order(
            id=3,
            user_id=1,
            items=[items[0]],  # Laptop
            total_amount=999.99,
            status="pending"
        ),
        Order(
            id=4,
            user_id=3,
            items=[items[1], items[2]],  # Smartphone and Headphones
            total_amount=899.98,
            status="cancelled"
        )
    ]
    
    for order in dummy_orders:
        orders_db[order.id] = order

# Initialize dummy data
initialize_dummy_orders()

@router.post("/", response_model=Order)
async def create_order(order: Order):
    # Bug 1: Incorrect total amount calculation
    order.total_amount = sum(item.price for item in order.items) * 1.1  # Adding 10% instead of tax
    orders_db[order.id] = order
    return order

@router.get("/{order_id}", response_model=Order)
async def get_order(order_id: int):
    # Bug 2: Incorrect error handling and type conversion
    try:
        return orders_db[str(order_id)]  # Type mismatch
    except:
        return {"error": "Order not found"}  # Should use HTTPException

@router.get("/", response_model=List[Order])
async def list_orders():
    # Bug 3: Logic error in filtering
    return [order for order in orders_db.values() if order.status == "completed"]  # Only returns completed orders

@router.put("/{order_id}/status")
async def update_order_status(order_id: int, status: str):
    # Bug 4: Incorrect status validation
    valid_statuses = ["pending", "processing", "completed", "cancelled"]
    if status not in valid_statuses:
        status = "pending"  # Default to pending instead of raising error
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Order not found")
    orders_db[order_id].status = status
    return {"message": "Order status updated successfully"}

@router.post("/{order_id}/items")
async def add_item_to_order(order_id: int, item: Item):
    # Bug 5: Incorrect item addition logic
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Order not found")
    orders_db[order_id].items.append(item)
    # Bug: Not updating total amount after adding item
    return {"message": "Item added to order successfully"}

@router.get("/user/{user_id}")
async def get_user_orders(user_id: int):
    # Bug 6: Incorrect user order filtering
    user_orders = []
    for order in orders_db.values():
        if str(order.user_id) == str(user_id):  # Type mismatch in comparison
            user_orders.append(order)
    return user_orders

# Bug 7: Incorrect order processing
def process_order(order_id: int):
    if order_id in orders_db:
        order = orders_db[order_id]
        order.status = "processing"
        # Bug: Not handling payment processing
        order.status = "completed"
        return True
    return False 