from typing import Optional

from .player_service import PlayerService
from ..abc_repositories import TournamentABCRepository
from ..models import Tournament, Player
from ...errors.tournament_errors import TournamentDoesNotExistsError, TournamentNoSlotsError
from ...schemas import TournamentCreate, TournamentRead, PlayerRegister


class TournamentService:
    __slots__ = (
            "__tournament_orm",
            "__player_service",
    )

    def __init__(
            self,
            tournament_orm: TournamentABCRepository,
            player_service: Optional[PlayerService] = None
    ) -> None:
        self.__tournament_orm = tournament_orm
        self.__player_service = player_service

    async def create_tournament(
            self,
            tournament_dto: TournamentCreate,
    ) -> TournamentRead:
        tournament = await self.__tournament_orm.create_tournament(
            tournament_dto=tournament_dto,
        )
        return tournament

    async def register_player(
            self,
            tournament_id: int,
            player_dto: PlayerRegister,
    ) -> TournamentRead:

        tournament = await self._get_tournament_or_raise(
            tournament_id=tournament_id,
        )
        await self._validate_slot_availability(
            tournament=tournament,
        )

        player = await self.__player_service.register_player(
            tournament=tournament,
            player_dto=player_dto,
        )

    @staticmethod
    async def _validate_slot_availability(
            tournament: Tournament,
    ) -> None:
        if tournament.registered_players == tournament.max_players:
            raise TournamentNoSlotsError(
                message=f"Tournament with id={tournament.id} has no slots."
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
