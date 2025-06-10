from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..domain.services import TournamentService
from ..infrastructure.database import get_db
from ..infrastructure.orm import TournamentORMRepository


async def get_tournament_service(
    session: AsyncSession = Depends(get_db),
) -> TournamentService:
    tournament_repository = TournamentORMRepository(
        session=session,
    )
    tournament_service = TournamentService(
        tournament_orm=tournament_repository,
    )
    return tournament_service
