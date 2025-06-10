from abc import ABC, abstractmethod
from typing import Union

from ..models import Tournament, Player
from ...schemas import TournamentCreate, PlayerRegister


class TournamentABCRepository(ABC):

    @abstractmethod
    async def create_tournament(
            self,
            tournament_dto: TournamentCreate,
    ) -> Tournament:
        raise NotImplementedError("Must be implemented by subclass")

    async def get_tournament(
            self,
            tournament_id: int,
            **kwargs,
    ) -> Union[Tournament, None]:
        raise NotImplementedError("Must be implemented by subclass")

    @abstractmethod
    async def register_player(
            self,
            tournament: Tournament,
            player_dto: PlayerRegister
    ) -> Tournament:
        raise NotImplementedError("Must be implemented by subclass")

    @abstractmethod
    async def get_players(
            self,
            tournament_id: int,
    ) -> list[Player]:
        raise NotImplementedError("Must be implemented by subclass")
