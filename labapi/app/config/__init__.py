from pydantic import BaseSettings


class CommonsSettings(BaseSettings):
    APP_NAME: str = "FARM Intro"
    DEBUG_MODE: bool = True


class ServerSettings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000


class DatabaseSettings(BaseSettings):
    DB_URL: str = "mongodb://10.253.4.75:27017/admin?w=majority&readPreference=primary&retryWrites=true&directConnection=true&ssl=false"
    DB_NAME: str = "mpee"
    DB_USER: str = "admin"
    DB_PASSWORD: str = "password"


class Settings(CommonsSettings, ServerSettings, DatabaseSettings):
    pass


from uuid import UUID
from pydantic import BaseModel, Field


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class ProfileUserModel(BaseModel):
    name: str = Field(...)
    email: str = Field(...)
    phone_number: str = Field(...)
    gender: str = Field(...)
    birth_date: str = Field(...)
    country: str = Field(...)
    ort: str = Field(...)

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
            }
        }

class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None


class UserAuth(BaseModel):
    email: str = Field(..., description="user email")
    password: str = Field(..., min_length=5, max_length=24, description="user password")


class DeleteUser(BaseModel):
    email: str = Field(..., description="user email")


class UserOut(BaseModel):
    id: UUID
    email: str


class Adrdata(BaseModel):
    adr_id: str


class Testdata(BaseModel):
    _id: UUID
    adr_time: int
    adr_int: int
    name: str
    project_id: str
    material_id: str
    adr52_1: int
    adr52_2: int
    adr80_1: int
    adr80_2: int
    adr80_3: int
    adr45_1: int
    adr45_2: int
    adr45_3: int
    adr45_4: int
    adr45_5: int
    adr45_6: int
    adr45_7: int
    adr45_8: int
    adr45_9: int
    adr45_10: int
    adr45_11: int
    adr45_12: int
    adr45_13: int
    adr45_14: int
    adr45_15: int
    adr45_16: int
    adr45_17: int
    adr45_18: int
    adr45_19: int
    adr45_20: int
    adr45_21: int
    adr45_22: int
    adr45_23: int
    adr46_1: int
    adr46_2: int
    adr46_3: int
    adr46_4: int
    adr46_5: int
    adr46_6: int
    adr46_7: int
    adr46_8: int
    adr46_9: int
    adr46_10: int
    adr46_11: int
    adr46_12: int
    adr46_13: int
    adr46_14: int
    adr46_15: int
    adr46_16: int
    adr50_1: int
    adr50_2: int
    adr50_3: int
    adr50_4: int
    adr50_5: int
    adr50_6: int
    adr50_7: int
    adr50_8: int
    adr50_9: int
    adr73_1: int
    adr73_2: int
    adr73_3: int
    adr73_4: int
    adr73_5: int
    adr73_6: int
    adr75_1: int
    adr75_2: int
    adr75_3: int
    adr75_4: int
    adr75_5: int
    adr75_6: int
    adr75_7: int
    adr75_8: int
    adr75_9: int
    adr75_10: int
    adr75_11: int
    adr75_12: int
    adr75_13: int
    adr75_14: int
    adr75_15: int
    adr75_16: int
    adr75_17: int
    adr75_18: int
    adr75_19: int
    adr75_20: int
    adr77_1: int
    adr77_2: int
    adr77_3: int
    adr77_4: int
    adr77_5: int
    adr77_6: int
    adr77_7: int
    adr77_8: int
    adr77_9: int
    id: UUID
    adr_id: str


class SystemUser(UserOut):
    password: str
    role: str


class Employee(BaseModel):
    id: int
    name: str
    product: list
    password: str
    created_date: str


class Admin(BaseModel):
    id: int
    name: str
    email: str
    password: str
    created_date: str
    last_login_date: str
    last_login_ort: str

settings = Settings()
