
from typing import Annotated

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    StringConstraints,
    field_validator
)


class UsuarioCriacao(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nome: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            min_length=1,
            max_length=150
        )
    ]

    email: EmailStr

    senha: str = Field(
        min_length=8,
        max_length=128
    )

    @field_validator("senha")
    @classmethod
    def validar_senha(cls, valor: str):
        if not valor.strip():
            raise ValueError(
                "A senha não pode conter apenas espaços."
            )

        return valor


class UsuarioSaida(BaseModel):
    id: int
    nome: str
    email: EmailStr
    perfil: str

    model_config = ConfigDict(from_attributes=True)
