from typing import Optional

from pydantic import EmailStr, Field

from .base_schema import BaseSchema


class PlayerCreate(BaseSchema):
    name: str = Field(..., example="Elnazar")
    email: EmailStr = Field(..., example="elnazar@example.com")


class PlayerRead(BaseSchema):
    name: str
    email: EmailStr


class PlayerRegister(BaseSchema):
    name: str = Field(..., example="Elnazar")
    email: EmailStr = Field(..., example="elnazar@example.com")
