from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from ..domain.services import TournamentService
from ..dependecies.services import get_tournament_service
from ..errors.tournament_errors import (
    TournamentDoesNotExistsError,
    TournamentNoSlotsError,
    PlayerAlreadyRegisteredError,
)
from ..schemas import (
    TournamentCreate,
    TournamentRead,
    PlayerRegister,
    PlayerRead,
)


tournament_router = APIRouter(
    prefix="/game",
    tags=["Tournament"],
)


@tournament_router.post(
    path="/tournaments",
    response_model=TournamentRead,
    summary="Create tournament",
)
async def create_tournament(
        tournament_data: TournamentCreate,
        tournament_service: TournamentService = Depends(get_tournament_service),
):
    tournament = await tournament_service.create_tournament(
        tournament_dto=tournament_data,
    )
    return tournament


@tournament_router.get(
    path="/tournaments/{tournament_id}/register",
    response_model=TournamentRead,
    summary="Register a player for a tournament",
)
async def register_player(
        player_data: PlayerRegister = Depends(),  # later update to Query()
        tournament_service: TournamentService = Depends(get_tournament_service),
):
    try:
        tournament = await tournament_service.register_player(
            player_dto=player_data,
        )
        return tournament
    except TournamentDoesNotExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except TournamentNoSlotsError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except PlayerAlreadyRegisteredError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@tournament_router.post(
    path="/tournaments/{tournament_id}/players",
    response_model=list[PlayerRead],
    summary="List tournament players",
)
async def list_players(
        tournament_id: int,
        tournament_service: TournamentService = Depends(get_tournament_service),
):
    try:
        players = await tournament_service.get_players(
            tournament_id=tournament_id,
        )
    except TournamentDoesNotExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    return players
