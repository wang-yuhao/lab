from typing import Optional, List

import uuid
from datetime import date
import time
from pydantic import BaseModel, Field


class ResponseUserModel(BaseModel):
    name: str = Field(...)
    id: str = Field(default_factory=uuid.uuid4, alias="_id")

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "name": "Xiao Ming",
                "id": "00010203-0405-0607-0809-0a0b0c0d0e0f",
            }
        }


class UserModel(BaseModel):
    name: str = Field(...)
    email: str = Field(...)
    phone_number: str = Field(...)
    gender: str = Field(...)
    birth_date: str = Field(...)
    country: str = Field(...)
    ort: str = Field(...)
    created_date: str = Field(...)
    last_login: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "name": "Xiao Ming",
                "email": "abcd@gmail.com",
                'phone_number': 1234567,
                'gender': "man",
                'birth_date': "2000-01-01",
                'created_date': "2000-01-01",
                'last_login': "2000-01-01",
                'country': "China",
                'ort': "Shanghai",
            }
        }

class ProfileUserModel(BaseModel):
    name: str = Field(...)
    email: str = Field(...)
    phone_number: str = Field(...)
    gender: str = Field(...)
    birth_date: str = Field(...)
    country: str = Field(...)
    ort: str = Field(...)
    role: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "name": "Xiao Ming",
                "email": "abcd@gmail.com",
                'phone_number': 1234567,
                'gender': "man",
                'birth_date': "2000-01-01",
                'country': "China",
                'ort': "Shanghai",
                'role': "customer",
            }
        }


class UserLoginModel():
    email: str = Field(...)
    password: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "email": "abcd@gmail.com",
                "password": "arztfhtrz567gfhf"
            }
        }

class CreateUserModel(BaseModel):
    name: str = Field(...)
    email: str = Field(...)
    role: str = Field(...)
    phone_number: str = Field(...)
    gender: str = Field(...)
    birth_date: str = Field(...)
    country: str = Field(...)
    ort: str = Field(...)
    password: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "name": "Xiao Ming",
                "email": "abcd@gmail.com",
                "role": "customer",
                'phone_number': "1234567",
                'gender': "man",
                'birth_date': "2000-01-01",
                'country': "China",
                'ort': "Shanghai",
                'password': "abcd@gmail.com"
            }
        }


class UpdateUserModel(BaseModel):
    name: str = Field(...)
    email: str = Field(...)
    role: str = Field(...)
    phone_number: str = Field(...)
    gender: str = Field(...)
    birth_date: str = Field(...)
    country: str = Field(...)
    ort: str = Field(...)
    password: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "name": "Xiao Ming",
                "email": "abcd@gmail.com",
                "role": "customer",
                'phone_number': 1234567,
                'gender': "man",
                'birth_date': "2000-01-01",
                'country': "China",
                'ort': "Shanghai",
                'password': "abcd@gmail.com"
            }
        }

