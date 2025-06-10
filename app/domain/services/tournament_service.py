from typing import Optional

from sqlalchemy.exc import IntegrityError

from ..abc_repositories import TournamentABCRepository
from ..models import Tournament, Player
from ...errors.tournament_errors import (
    TournamentDoesNotExistsError,
    TournamentNoSlotsError,
    PlayerAlreadyRegisteredError
)
from ...schemas import (
    TournamentCreate,
    TournamentRead,
    PlayerRegister,
    PlayerRead,
)


class TournamentService:
    __slots__ = (
            "__tournament_orm",
    )

    def __init__(
            self,
            tournament_orm: TournamentABCRepository,
    ) -> None:
        self.__tournament_orm = tournament_orm

    async def create_tournament(
            self,
            tournament_dto: TournamentCreate,
    ) -> TournamentRead:
        tournament = await self.__tournament_orm.create_tournament(
            tournament_dto=tournament_dto,
        )
        return TournamentRead.model_validate(tournament)

    async def register_player(
            self,
            player_dto: PlayerRegister,
    ) -> TournamentRead:

        tournament = await self._get_tournament_or_raise(
            tournament_id=player_dto.tournament_id,
        )
        await self._validate_slot_availability(
            tournament=tournament,
        )
        try:
            tournament = await self.__tournament_orm.register_player(
                tournament=tournament,
                player_dto=player_dto,
            )
        except IntegrityError:
            raise PlayerAlreadyRegisteredError(
                message=f"Player with email={player_dto.email} already registered."
            )
        return TournamentRead.model_validate(tournament)

    async def get_players(
            self,
            tournament_id: int,
    ):
        players_list: Optional[list[Player]] = await self.__tournament_orm.get_players(
            tournament_id=tournament_id,
        )
        if players_list is None:
            raise TournamentDoesNotExistsError(
                message=f"Tournament with id={tournament_id} does not exist."
            )
        return [PlayerRead.model_validate(player) for player in players_list]

    @staticmethod
    async def _validate_slot_availability(
            tournament: Tournament,
    ) -> None:
        if tournament.registered_players == tournament.max_players:
            raise TournamentNoSlotsError(
                message=f"Tournament with id={tournament.id} has no empty slots."
            )

    async def _get_tournament_or_raise(
            self,
            tournament_id: int,
    ) -> Tournament:
        tournament = await self.__tournament_orm.get_tournament(
            tournament_id=tournament_id,
            with_relationships=True,
        )

        if tournament is None:
            raise TournamentDoesNotExistsError(
                message=f"Tournament with id={tournament_id} does not exist."
            )
        return tournament
