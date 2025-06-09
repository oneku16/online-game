from __future__ import annotations

from datetime import datetime

from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ...infrastructure.database import Base


class Tournament(Base):
    __tablename__ = "tournaments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    max_players: Mapped[int] = mapped_column(Integer, nullable=False)
    registered_players: Mapped[int] = mapped_column(Integer, default=0)
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    players: Mapped[list["Player"]] = relationship(
        argument="Player",
        back_populates="tournament",
        cascade="all, delete-orphan",
    )
