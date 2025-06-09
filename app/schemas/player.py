from pydantic import EmailStr, Field

from .base_schema import BaseSchema


class PlayerCreate(BaseSchema):
    name: str = Field(..., example="Elnazar")
    email: EmailStr = Field(..., example="elnazar@example.com")


class PlayerRead(BaseSchema):
    name: str
    email: EmailStr


class PlayerRegister(BaseSchema):
    tournament_id: int = Field(..., example=1)
    name: str = Field(..., example="Elnazar")
    email: EmailStr = Field(..., example="elnazar@example.com")
