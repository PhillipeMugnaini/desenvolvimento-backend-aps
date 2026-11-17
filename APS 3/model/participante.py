
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from model.inscricao import Inscricao


class Participante(Base):
    __tablename__ = "participantes"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )

    nome: Mapped[str] = mapped_column(
        String(150), nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(254), unique=True, index=True, nullable=False
    )

    curso: Mapped[str] = mapped_column(
        String(150), nullable=False
    )

    inscricoes: Mapped[list["Inscricao"]] = relationship(
        "Inscricao",
        back_populates="participante",
        cascade="all, delete-orphan"
    )
