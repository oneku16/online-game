from datetime import datetime
from pydantic import Field

from .base_schema import BaseSchema


class TournamentCreate(BaseSchema):
    name: str = Field(..., example="Weekend Cup")
    max_players: int = Field(..., example=8)
    start_date: datetime = Field(..., example="2025-06-01T15:00:00Z")


class TournamentRead(BaseSchema):
    id: int
    name: str
    max_players: int
    start_date: datetime
