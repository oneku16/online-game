from abc import ABC, abstractmethod
from typing import Optional

from pydantic import EmailStr

from ..models import Player
from ...schemas import PlayerCreate


class PlayerABCRepository(ABC):
    @abstractmethod
    async def create_player(self, player_data: PlayerCreate) -> Player:
        raise NotImplementedError("Must be implemented in subclass")

    @abstractmethod
    async def get_player_by_email(self, email: EmailStr | str) -> Optional[Player]:
        raise NotImplementedError("Must be implemented in subclass")

    @abstractmethod
    async def get_player_by_id(self, id: int) -> Optional[Player]:
        raise NotImplementedError("Must be implemented in subclass")
