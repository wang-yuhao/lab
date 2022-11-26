from typing import Optional, List

import uuid
from datetime import date
import time
from pydantic import BaseModel, Field


class ProjectModel(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)
    project_id: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "id": "00010203-0405-0607-0809-0a0b0c0d0e0f",
                "name": "New ACME Soap spot",
                "project_id": "abcd",
            }
        }


class ProjectMetaModel(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)
    project_id: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "id": "00010203-0405-0607-0809-0a0b0c0d0e0f",
                "name": "New ACME Soap spot",
                "project_id": "abcd",
            }
        }


class UpdateProjectModel(BaseModel):
    name: Optional[str]

    project_id: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "name": "My project"
            }
        }