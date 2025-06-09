from typing import Optional

from ..abc_repositories import PlayerABCRepository, TournamentABCRepository
from ...schemas import TournamentRead, PlayerRegister
from ...domain.models import Tournament
from ...errors.player_errors import PlayerAlreadyRegistered


class PlayerService:
    __slots__ = ('__player_orm',)

    def __init__(
            self,
            player_orm: PlayerABCRepository,
    ) -> None:
        self.__player_orm = player_orm

    async def register_player(
            self,
            player_dto: PlayerRegister,
            tournament: Tournament,
    ) -> TournamentRead:
        await self.__player_orm.register_player(
            player_dto=player_dto,
            tournament=tournament,
        )
