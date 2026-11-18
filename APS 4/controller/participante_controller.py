from fastapi import APIRouter, HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db

from schema.participante_schema import Participante, ParticipanteEntrada
from service.participante_service import (
    cadastrar_participante,
    listar_participantes,
    buscar_participante_por_id,
    atualizar_participante,
    excluir_participante,
    EmailDuplicadoError
)

from security.dependencies import (
    obter_usuario_atual,
    exigir_administrador
)

router = APIRouter()

@router.post(
    "/participantes",
    response_model=Participante,
    status_code=201,
    dependencies=[Depends(exigir_administrador)]
)
def criar_participante(
    dados: ParticipanteEntrada,
    db: Session = Depends(get_db)
):
    participante = cadastrar_participante(dados, db)

    if participante is None:
        raise HTTPException(
            status_code=409,
            detail="Já existe um participante cadastrado com este e-mail."
        )

    return participante


@router.get(
    "/participantes",
    response_model=list[Participante],
    dependencies=[Depends(obter_usuario_atual)]
)
def obter_participantes(
    db: Session = Depends(get_db)
):
    return listar_participantes(db)

@router.get(
    "/participantes/{participante_id}",
    response_model=Participante,
    dependencies=[Depends(obter_usuario_atual)]
)
def obter_participante(
    participante_id: int,
    db: Session = Depends(get_db)
):
    participante = buscar_participante_por_id(participante_id, db)

    if participante is None:
        raise HTTPException(
            status_code=404,
            detail="Participante não encontrado."
        )

    return participante


@router.put(
    "/participantes/{participante_id}",
    response_model=Participante,
    dependencies=[Depends(exigir_administrador)]
)
def editar_participante(
    participante_id: int,
    dados: ParticipanteEntrada,
    db: Session = Depends(get_db)
):
    try:
        participante = atualizar_participante(
            participante_id, dados, db
        )

    except EmailDuplicadoError:
        raise HTTPException(
            status_code=409,
            detail="Já existe um participante cadastrado com este e-mail."
        )

    if participante is None:
        raise HTTPException(
            status_code=404,
            detail="Participante não encontrado."
        )

    return participante


@router.delete(
    "/participantes/{participante_id}",
    status_code=204,
    dependencies=[Depends(exigir_administrador)]
)
def remover_participante(
    participante_id: int,
    db: Session = Depends(get_db)
):
    removido = excluir_participante(participante_id, db)

    if not removido:
        raise HTTPException(
            status_code=404,
            detail="Participante não encontrado."
        )
