from typing import Optional, Union
from time import sleep

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from . import queries
from ...domain.models import Tournament, Player
from ...domain.abc_repositories import TournamentABCRepository
from ...errors.tournament_errors import TournamentDoesNotExistsError, TournamentNoSlotsError
from ...errors.player_errors import PlayerAlreadyRegistered
from ...schemas import PlayerRead, PlayerRegister, TournamentCreate, TournamentRead


class TournamentORMRepository(TournamentABCRepository):
    __slots__ = ("__session",)

    def __init__(self, session: AsyncSession):
        self.__session = session

    async def create_tournament(
            self,
            tournament_dto: TournamentCreate,
    ) -> TournamentRead:
        tournament: Optional[Tournament] = Tournament(
            **tournament_dto.model_dump(),
        )
        async with self.__session as session:
            session.add(tournament)
            await session.commit()
            await session.refresh(tournament)
            sleep(seconds=.1)
            return TournamentRead.model_validate(tournament)

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
        tournament_id: int,
        player_dto: PlayerRegister,
    ) -> TournamentRead:
        async with self.__session as session:

            player = Player(
                **player_dto.model_dump(),
                tournament_id=tournament_id,
            )

            session.add(player)
            tournament.registered_players += 1

            try:
                await session.commit()
            except IntegrityError:
                await session.rollback()
                raise PlayerAlreadyRegistered(
                    message=f"Player with email={player_dto.email} already registered."
                )

            return TournamentRead.model_validate(tournament)

    @staticmethod
    async def _get_tournament_or_raise(tournament_id: int, session: AsyncSession) -> Tournament:
        tournament = await queries.get_tournament_by_id(id=tournament_id, session=session)
        if tournament is None:
            raise TournamentDoesNotExistsError(
                message=f"Tournament with id={tournament_id} does not exist."
            )
        return tournament

    @staticmethod
    def _validate_slot_availability(tournament: Tournament) -> None:
        if tournament.registered_players >= tournament.max_players:
            raise TournamentNoSlotsError(
                message=f"Tournament with id={tournament.id} has no slots."
            )

    async def get_players(
            self,
            tournament_id: int,
    ) -> list[PlayerRead]:
        async with self.__session as session:
            tournament: Optional[Tournament] = await queries.get_tournament_by_id(
                id=tournament_id,
                session=session,
                with_relationships=True,
            )
            if tournament is None:
                raise TournamentDoesNotExistsError(
                    message=f"Tournament with id={tournament_id} does not exist."
                )

            return [PlayerRead.model_validate(player) for player in tournament.players]
