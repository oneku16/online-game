from abc import ABC, abstractmethod
from typing import Union


from ..models import Tournament
from ...schemas import PlayerCreate, TournamentCreate


class PlayerABCRepository(ABC):

    @abstractmethod
    async def register_player(
            self,
            player_dto: PlayerCreate,
            tournament_dto: Tournament,
    ) -> Union[Tournament, None]:
        raise NotImplementedError("Must be implemented in subclass")
