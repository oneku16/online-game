from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..domain.models import Player
from ..domain.services import PlayerService
from ..errors.player_errors import PlayerAlreadyExists
from ..infrastructure.orm import PlayerORMRepository
from ..infrastructure.database import get_db
from ..schemas import PlayerCreate, PlayerRead


player_router = APIRouter(
    prefix="/player",
)


@player_router.post(
    path="/register",
    response_model=PlayerRead,
    tags=["Players"],
)
async def register_player(
        player_data: PlayerCreate,
        database: AsyncSession = Depends(get_db),
):
    player_service: PlayerService = PlayerService(
        player_orm=PlayerORMRepository(
            session=database,
        ),
    )
    try:
        player: PlayerRead = await player_service.create_player(player_data)
        return player
    except PlayerAlreadyExists as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{e}",
        )




