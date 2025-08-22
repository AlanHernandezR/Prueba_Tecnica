from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, field_serializer

class ItemCreate(BaseModel):
    name: str
    price: float

class OrderCreate(BaseModel):
    customer_name: str
    items: List[ItemCreate]

class ItemRead(BaseModel):
    id: int
    name: str
    price: float

    class Config:
        from_attributes = True

class OrderRead(BaseModel):
    id: int
    customer_name: str
    created_at: datetime
    items: List[ItemRead]
    
    @field_serializer('created_at')
    def serialize_datetime(self, dt: datetime):
        return dt.isoformat()

    class Config:
        from_attributes = True