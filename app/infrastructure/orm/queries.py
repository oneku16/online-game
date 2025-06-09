from typing import Union

from sqlalchemy import desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from ...domain.models import Player, Tournament


async def get_player_by_id(
        id: int,
        session: AsyncSession,
) -> Union[Player, None]:
    result = await session.execute(
        select(Player)
        .where(Player.id == id)
    )
    return result.scalar_one_or_none()


async def get_player_by_email(
        email: str,
        session: AsyncSession,
) -> Union[Player, None]:
    result = await session.execute(
        select(Player)
        .where(Player.email == email)
    )
    return result.scalar_one_or_none()


async def get_tournament_by_id(
        id: int,
        session: AsyncSession,
        *,
        with_relationships: bool = False,
) -> Union[Tournament, None]:
    if with_relationships:
        selector = (
                select(Tournament)
                .where(Tournament.id == id)
                .options(selectinload(Tournament.players))
        )
    else:
        selector = (
                select(Tournament)
                .where(Tournament.id == id)
        )
    result = await session.execute(selector)
    return result.scalar_one_or_none()
