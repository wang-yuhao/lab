from typing import Optional, List
import uuid
from pydantic import BaseModel, Field


class KPIDataModel(BaseModel):
    id : str = Field(default_factory=uuid.uuid4, alias="_id")
    type : str = Field(...)
    platform : str = Field(...)
    cleaned_value : str = Field(...)
    interval : str = Field(...)
    created_at : str = Field(...)
    updated_at : str = Field(...)
    testPerson : str = Field(...)
    adr_time : str = Field(...)
    testPersonId : str = Field(...)
    gender : str = Field(...)
    age : str = Field(...)
    adr_id : str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "id": "01a593af-4eed-4fc1-915b-98adf811a4d3",
                "type": "liking",
                "platform": "TV",
                "cleaned_value": 1.631377009,
                "interval": 1,
                "created_at": "2022-02-09T11:21:50.103000+01:00",
                "updated_at": "2022-02-09T11:21:50.103000+01:00",
                "testPerson": 4222,
                "adr_time": 5.0,
                "testPersonId": 5,
                "gender": "m",
                "age": 54,
                "adr_id": "0045 - Maoam - Wer stiehlt mir die Show_21225113_Dis_Maoam"
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