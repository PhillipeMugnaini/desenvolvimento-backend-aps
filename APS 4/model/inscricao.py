
from datetime import datetime, timezone

from sqlalchemy import ForeignKey, UniqueConstraint, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from model.evento import Evento
    from model.participante import Participante


class Inscricao(Base):
    __tablename__ = "inscricoes"

    __table_args__ = (
        UniqueConstraint(
            "evento_id",
            "participante_id",
            name="uq_inscricao_evento_participante"
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    evento_id: Mapped[int] = mapped_column(
        ForeignKey("eventos.id"),
        nullable=False
    )

    participante_id: Mapped[int] = mapped_column(
        ForeignKey("participantes.id"),
        nullable=False
    )

    data_inscricao: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    evento: Mapped["Evento"] = relationship(
        "Evento",
        back_populates="inscricoes"
    )

    participante: Mapped["Participante"] = relationship(
        "Participante",
        back_populates="inscricoes"
    )
