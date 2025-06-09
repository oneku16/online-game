from __future__ import annotations

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ...infrastructure.database import Base


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
