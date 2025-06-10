from abc import ABC, abstractmethod
from typing import Any

from ...schemas import PlayerRegister, TournamentCreate
from ..models import Player, Tournament


class TournamentABCRepository(ABC):

    @abstractmethod
    async def create_tournament(
        self,
        tournament_dto: TournamentCreate,
    ) -> Tournament:
        raise NotImplementedError("Must be implemented by subclass")

    async def get_tournament(
        self, tournament_id: int, **kwargs: Any
    ) -> Tournament | None:
        raise NotImplementedError("Must be implemented by subclass")

    @abstractmethod
    async def register_player(
        self, tournament: Tournament, player_dto: PlayerRegister
    ) -> Tournament:
        raise NotImplementedError("Must be implemented by subclass")

    @abstractmethod
    async def get_players(
        self,
        tournament_id: int,
    ) -> list[Player] | None:
        raise NotImplementedError("Must be implemented by subclass")
