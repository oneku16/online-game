from typing import Optional

from ..abc_repositories import PlayerABCRepository
from ...schemas import PlayerCreate, PlayerRead
from ...errors.player_errors import PlayerAlreadyExists
from ...domain.models import Player


class PlayerService:
    __slots__ = ('__player_orm',)

    def __init__(self, player_orm: PlayerABCRepository) -> None:
        self.__player_orm = player_orm

    async def create_player(self, player_data: PlayerCreate) -> PlayerRead:
        existing_player = await self.__player_orm.get_player_by_email(player_data.email)
        if existing_player:
            raise PlayerAlreadyExists(
                message=f"Player with {existing_player.email} is already exists.",
            )
        player: Optional[Player] = await self.__player_orm.create_player(
            player_data=player_data,
        )
        return PlayerRead.model_validate(player)
