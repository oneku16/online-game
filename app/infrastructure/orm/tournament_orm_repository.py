from typing import Optional, Union

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from . import queries
from ...domain.models import Tournament, Player
from ...domain.abc_repositories import TournamentABCRepository
from ...schemas import (
    PlayerRegister,
    TournamentCreate,
)


class TournamentORMRepository(TournamentABCRepository):
    __slots__ = ("__session",)

    def __init__(
            self, session: AsyncSession,
    ) -> None:
        self.__session = session

    async def create_tournament(
            self,
            tournament_dto: TournamentCreate,
    ) -> Tournament:
        tournament: Optional[Tournament] = Tournament(
            **tournament_dto.model_dump(),
        )
        async with self.__session as session:
            session.add(tournament)
            await session.commit()
            await session.refresh(tournament)
            return tournament

    async def get_tournament(
            self,
            tournament_id: int,
            **kwargs
    ) -> Union[Tournament, None]:
        async with self.__session as session:
            tournament = await queries.get_tournament_by_id(
                id=tournament_id,
                session=session,
                **kwargs,
            )
            return tournament

    async def register_player(
        self,
        tournament: Tournament,
        player_dto: PlayerRegister,
    ) -> Tournament:
        async with self.__session as session:

            player = Player(
                **player_dto.model_dump(),
            )

            session.add(player)
            tournament.registered_players += 1
            session.add(tournament)

            try:
                await session.commit()
            except IntegrityError as e:
                await session.rollback()
                raise e

            return tournament

    async def get_players(
            self,
            tournament_id: int,
    ) -> Union[list[Player], None]:
        async with self.__session as session:
            tournament: Optional[Tournament] = await queries.get_tournament_by_id(
                id=tournament_id,
                session=session,
                with_relationships=True,
            )
            if tournament is None:
                raise None

            return [player for player in tournament.players]
