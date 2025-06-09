from abc import ABC, abstractmethod
from typing import Union

from ..models import Tournament
from ...schemas import TournamentCreate, TournamentRead, PlayerRegister, PlayerRead


class TournamentABCRepository(ABC):

    @abstractmethod
    async def create_tournament(
            self,
            tournament_dto: TournamentCreate,
    ) -> TournamentRead:
        raise NotImplementedError("Must be implemented by subclass")

    async def get_tournament(
            self,
            tournament_id: int,
            with_relationships=True
    ) -> Union[Tournament, None]:
        raise NotImplementedError("Must be implemented by subclass")

    @abstractmethod
    async def register_player(
            self,
            tournament_id: int,
            player_dto: PlayerRegister
    ) -> PlayerRegister:
        raise NotImplementedError("Must be implemented by subclass")

    @abstractmethod
    async def get_players(
            self,
            tournament_id: int,
    ) -> list[PlayerRead]:
        raise NotImplementedError("Must be implemented by subclass")
