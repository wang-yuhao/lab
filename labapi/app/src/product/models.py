from typing import Optional, List

import uuid
from datetime import date
import time
from pydantic import BaseModel, Field


class ProductModel(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    status: str = Field(...)
    employee_id: str = Field(...)
    created_date: str = Field(...)
    product_id: int = Field(...)
    product_name: str = Field(...)
    price: int = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "id": "00010203-0405-0607-0809-0a0b0c0d0e0f",
                "status": "paid",
                "product_id": 1234567,
                "product_name": "32tre432-0405-0607-0809-rewr233243256",
                "employee_id": "435647754-0405-0607-0809-gft4364334546",
                "created_date": "2022-01-01",
                "price": 245
            }
        }


class UpdateProductModel(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    status: str = Field(...)
    employee_id: str = Field(...)
    created_date: str = Field(...)
    product_id: int = Field(...)
    product_name: str = Field(...)
    price: int = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "id": "00010203-0405-0607-0809-0a0b0c0d0e0f",
                "status": "paid",
                "product_id": 1234567,
                "product_name": "32tre432-0405-0607-0809-rewr233243256",
                "employee_id": "435647754-0405-0607-0809-gft4364334546",
                "created_date": "2022-01-01",
                "price": 245
            }
        }