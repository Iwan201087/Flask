import datetime

from pydantic import BaseModel, Field


class User(BaseModel):
    id: int = None
    name: str = Field(..., max_length=32)
    surname: str = Field(max_length=48)
    email: str = Field(..., max_length=128)
    password: str = Field(..., min_length=6, max_length=255)


class Order(BaseModel):
    id: int = None
    user_id: int
    product_id: int
    date: datetime.datetime = datetime.datetime.now()
    status: str = Field(..., max_length=48)


class Product(BaseModel):
    id: int = None
    name: str = Field(..., max_length=32)
    description: str = Field(None, max_length=128)
    price: float = Field(..., gt=0)