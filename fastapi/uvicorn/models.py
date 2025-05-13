from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class User(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)

class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    owner_id: int

class Order(BaseModel):
    id: int
    user_id: int
    items: List[Item]
    total_amount: float
    status: str = "pending" 