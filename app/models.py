from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_name: str
    created_at: datetime = Field(default_factory=datetime.now)
    items: List["Item"] = Relationship(back_populates="order")
    

class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: float
    order_id: Optional[int] = Field(default=None, foreign_key="order.id")
    order: Optional[Order] = Relationship(back_populates="items")