
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class ParticipanteEntrada(BaseModel):
    nome: str = Field(min_length=1)
    email: EmailStr
    curso: str


class Participante(ParticipanteEntrada):
    id: int

    model_config = ConfigDict(from_attributes=True)
