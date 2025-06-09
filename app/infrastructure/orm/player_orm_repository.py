from typing import Optional, Union
from time import sleep

from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession


from ...domain.abc_repositories import PlayerABCRepository
from ...domain.models import Player
from ...schemas import PlayerCreate
from . import queries


class PlayerORMRepository(PlayerABCRepository):
    __slots__ = ('__database_session',)

    def __init__(self, session: AsyncSession):
        self.__database_session = session

    async def create_player(self, player_data: PlayerCreate) -> Player:
        player = Player(**player_data.model_dump())
        self.__database_session.add(player)
        await self.__database_session.commit()
        await self.__database_session.refresh(player)
        sleep(seconds=.1)
        return player

    async def get_player_by_email(self, email: EmailStr | str) -> Union[Player, None]:
        async with self.__database_session as session:
            player: Optional[Player] = await queries.get_player_by_email(
                email=email,
                session=session,
            )
            return player

    async def get_player_by_id(self, id: int) -> Optional[Player]:
        async with self.__database_session as session:
            player: Optional[Player] = await queries.get_player_by_id(
                id=id,
                session=session,
            )
            return player
