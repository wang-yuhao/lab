from typing import Optional, List

import uuid
from datetime import date
import time
from pydantic import BaseModel, Field


class EmployeeModel(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    status: str = Field(...)
    name: str = Field(...)
    email: str = Field(...)
    phone_number: str = Field(...)
    gender: str = Field(...)
    birth_date: str = Field(...)
    created_date: str = Field(...)
    last_login: str = Field(...)
    country: str = Field(...)
    ort: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "id": "00010203-0405-0607-0809-0a0b0c0d0e0f",
                "name": "Xiao Ming",
                "email": "abcd@gmail.com",
            }
        }


class UpdateEmployeeModel(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    status: str = Field(...)
    name: str = Field(...)
    email: str = Field(...)
    phone_number: str = Field(...)
    gender: str = Field(...)
    birth_date: str = Field(...)
    created_date: str = Field(...)
    country: str = Field(...)
    ort: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "id": "00010203-0405-0607-0809-0a0b0c0d0e0f",
                "name": "Xiao Ming",
                "email": "abcd@gmail.com",
            }
        }

