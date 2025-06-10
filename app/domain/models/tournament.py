from datetime import datetime

from sqlalchemy import String, Integer, UniqueConstraint, ForeignKey, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ...infrastructure.database import Base


class Tournament(Base):
    __tablename__ = "tournaments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    max_players: Mapped[int] = mapped_column(Integer, nullable=False)
    registered_players: Mapped[int] = mapped_column(Integer, default=0)
    start_date: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
    )

    players: Mapped[list["Player"]] = relationship(
        back_populates="tournament",
        cascade="all, delete-orphan",
    )


class Player(Base):
    __tablename__ = "players"
    __table_args__ = (UniqueConstraint(
        "tournament_id",
        "email",
        name="uq_tournament_email"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(128))
    email: Mapped[str] = mapped_column(String(128), index=True)

    tournament_id: Mapped[int] = mapped_column(ForeignKey("tournaments.id"))

    tournament: Mapped["Tournament"] = relationship(
        back_populates="players"
    )
