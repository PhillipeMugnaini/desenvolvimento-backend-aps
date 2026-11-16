from fastapi import APIRouter, HTTPException

from model.participante import Participante, ParticipanteEntrada
from service.participante_service import (
    cadastrar_participante,
    listar_participantes,
    buscar_participante_por_id,
    atualizar_participante,
    excluir_participante
)


router = APIRouter()


@router.post("/participantes", response_model=Participante, status_code=201)
def criar_participante(dados: ParticipanteEntrada):
    return cadastrar_participante(dados)


@router.get("/participantes", response_model=list[Participante])
def obter_participantes():
    return listar_participantes()


@router.get("/participantes/{participante_id}", response_model=Participante)
def obter_participante(participante_id: int):
    participante = buscar_participante_por_id(participante_id)

    if participante is None:
        raise HTTPException(
            status_code=404,
            detail="Participante não encontrado."
        )

    return participante

@router.put("/participantes/{participante_id}", response_model=Participante)
def editar_participante(participante_id: int, dados: ParticipanteEntrada):
    participante = atualizar_participante(participante_id, dados)

    if participante is None:
        raise HTTPException(
            status_code=404,
            detail="Participante não encontrado."
        )

    return participante

@router.delete("/participantes/{participante_id}", status_code=204)
def remover_participante(participante_id: int):
    removido = excluir_participante(participante_id)

    if not removido:
        raise HTTPException(
            status_code=404,
            detail="Participante não encontrado."
        )