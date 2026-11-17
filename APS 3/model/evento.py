
from datetime import date, time

from sqlalchemy import Date, Integer, String, Text, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from model.inscricao import Inscricao


class Evento(Base):
    __tablename__ = "eventos"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )

    titulo: Mapped[str] = mapped_column(
        String(200), nullable=False
    )

    descricao: Mapped[str] = mapped_column(
        Text, nullable=False
    )

    data: Mapped[date] = mapped_column(
        Date, nullable=False
    )

    horario: Mapped[time] = mapped_column(
        Time, nullable=False
    )

    local: Mapped[str] = mapped_column(
        String(200), nullable=False
    )

    capacidade: Mapped[int] = mapped_column(
        Integer, nullable=False
    )

    categoria: Mapped[str] = mapped_column(
        String(80), nullable=False
    )

    inscricoes: Mapped[list["Inscricao"]] = relationship(
        "Inscricao",
        back_populates="evento",
        cascade="all, delete-orphan"
    )
