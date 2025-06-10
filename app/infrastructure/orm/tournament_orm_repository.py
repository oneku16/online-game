from typing import Any

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from ...domain.abc_repositories import TournamentABCRepository
from ...domain.models import Player, Tournament
from ...schemas import (
    PlayerRegister,
    TournamentCreate,
)
from . import queries


class TournamentORMRepository(TournamentABCRepository):
    __slots__ = ("__session",)

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.__session = session

    async def create_tournament(
        self,
        tournament_dto: TournamentCreate,
    ) -> Tournament:
        tournament: Tournament | None = Tournament(
            **tournament_dto.model_dump(),
        )
        async with self.__session as session:
            session.add(tournament)
            await session.commit()
            await session.refresh(tournament)
            return tournament  # type: ignore[return-value]

    async def get_tournament(
        self,
        tournament_id: int,
        **kwargs: Any,
    ) -> Tournament | None:
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
    ) -> list[Player] | None:
        async with self.__session as session:
            tournament: Tournament | None = await queries.get_tournament_by_id(
                id=tournament_id,
                session=session,
                with_relationships=True,
            )
            if tournament is None:
                return None

            return [player for player in tournament.players]
