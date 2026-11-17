from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from database import get_db
from schema.inscricao_schema import InscricaoSaida
from schema.participante_schema import Participante as ParticipanteSaida
from service.inscricao_service import (
    inscrever_participante,
    listar_inscritos
)


router = APIRouter()



@router.post(
    "/eventos/{evento_id}/inscricoes/{participante_id}",
    response_model=InscricaoSaida,
    status_code=201
)
def criar_inscricao(
    evento_id: int,
    participante_id: int,
    db: Session = Depends(get_db)
):
    resultado = inscrever_participante(
        evento_id,
        participante_id,
        db
    )

    if isinstance(resultado, dict) and "erro" in resultado:
        erros = {
            "evento_nao_encontrado": (
                404, "Evento não encontrado."
            ),
            "participante_nao_encontrado": (
                404, "Participante não encontrado."
            ),
            "participante_ja_inscrito": (
                409, "Participante já está inscrito neste evento."
            ),
            "evento_sem_vagas": (
                409, "Não existem vagas disponíveis para este evento."
            ),
            "conflito_integridade": (
                409, "Conflito ao registrar a inscrição."
            )
        }

        status, mensagem = erros[resultado["erro"]]

        raise HTTPException(
            status_code=status,
            detail=mensagem
        )

    return resultado



@router.get(
    "/eventos/{evento_id}/inscricoes",
    response_model=list[ParticipanteSaida]
)
def obter_inscritos(
    evento_id: int,
    db: Session = Depends(get_db)
):
    participantes = listar_inscritos(evento_id, db)

    if participantes is None:
        raise HTTPException(
            status_code=404,
            detail="Evento não encontrado."
        )

    return participantes
