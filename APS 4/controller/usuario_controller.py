
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db

from schema.usuario_schema import (
    UsuarioCriacao,
    UsuarioSaida
)

from service.usuario_service import (
    cadastrar_usuario,
    EmailUsuarioDuplicadoError
)


router = APIRouter(
    prefix="/usuarios",
    tags=["Usuários"]
)


@router.post(
    "",
    response_model=UsuarioSaida,
    status_code=201
)
def criar_usuario(
    dados: UsuarioCriacao,
    db: Session = Depends(get_db)
):
    try:
        usuario = cadastrar_usuario(dados, db)

    except EmailUsuarioDuplicadoError:
        raise HTTPException(
            status_code=409,
            detail="Já existe um usuário cadastrado com este e-mail."
        )

    return usuario
