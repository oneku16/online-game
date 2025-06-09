from typing import Union

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from ...domain.abc_repositories import PlayerABCRepository
from ...domain.models import Player, Tournament
from ...schemas import PlayerCreate


class PlayerORMRepository(PlayerABCRepository):
    __slots__ = ('__session',)

    def __init__(self, session: AsyncSession):
        self.__session = session

    async def register_player(
            self,
            player_dto: PlayerCreate,
            tournament: Tournament,
    ) -> Union[Tournament, None]:
        async with self.__session as session:

            player = Player(
                **player_dto.model_dump(),
                tournament_id=tournament.id,
            )

            session.add(player)
            tournament.registered_players += 1

            try:
                await session.commit()
            except IntegrityError as e:
                await session.rollback()
                raise e

            return tournament
