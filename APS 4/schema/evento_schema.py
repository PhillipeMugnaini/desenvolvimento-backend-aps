from pydantic import BaseModel, Field, ConfigDict
from datetime import date, time


class EventoEntrada(BaseModel):
    titulo: str = Field(min_length=1)
    descricao: str
    data: date
    horario: time
    local: str
    capacidade: int = Field(gt=0)
    categoria: str


class Evento(EventoEntrada):
    id: int

    model_config = ConfigDict(from_attributes=True)