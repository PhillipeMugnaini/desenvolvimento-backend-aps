from fastapi import APIRouter, HTTPException

from service.inscricao_service import (
    inscrever_participante,
    listar_inscritos
)

router = APIRouter()


@router.post("/eventos/{evento_id}/inscricoes/{participante_id}", status_code=201)
def criar_inscricao(evento_id: int, participante_id: int):
    resultado = inscrever_participante(evento_id, participante_id)

    if "erro" in resultado:
        if resultado["erro"] == "evento_nao_encontrado":
            raise HTTPException(
                status_code=404,
                detail="Evento não encontrado."
            )

        if resultado["erro"] == "participante_nao_encontrado":
            raise HTTPException(
                status_code=404,
                detail="Participante não encontrado."
            )

        if resultado["erro"] == "participante_ja_inscrito":
            raise HTTPException(
                status_code=400,
                detail="Participante já está inscrito neste evento."
            )

        if resultado["erro"] == "evento_sem_vagas":
            raise HTTPException(
                status_code=400,
                detail="Não existem vagas disponíveis para este evento."
            )

    return resultado

@router.get("/eventos/{evento_id}/inscricoes")
def obter_inscritos(evento_id: int):
    return listar_inscritos(evento_id)