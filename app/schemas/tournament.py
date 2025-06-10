from datetime import datetime

from pydantic import EmailStr, Field

from .base_schema import BaseSchema


class TournamentCreate(BaseSchema):
    name: str = Field(..., json_schema_extra={"example": "Weekend Cup"})
    max_players: int = Field(..., json_schema_extra={"example": 8})
    start_date: datetime = Field(
        ...,
        json_schema_extra={
            "example": "2020-06-01T15:00:00Z",
        },
    )


class TournamentRead(BaseSchema):
    id: int
    name: str
    max_players: int
    start_date: datetime
    registered_players: int


class PlayerRead(BaseSchema):
    name: str
    email: EmailStr


class PlayerRegister(BaseSchema):
    tournament_id: int = Field(..., json_schema_extra={"example": 1})
    name: str = Field(..., json_schema_extra={"example": "Elnazar"})
    email: EmailStr = Field(..., json_schema_extra={"example": "elnazar@example.com"})
