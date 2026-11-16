from fastapi import APIRouter, HTTPException
from model.evento import Evento, EventoEntrada
from service.evento_service import (
    cadastrar_evento,
    listar_eventos,
    buscar_evento_por_id,
    atualizar_evento,
    excluir_evento
)


router = APIRouter()


@router.post("/eventos", response_model=Evento, status_code=201)
def criar_evento(dados: EventoEntrada):
    return cadastrar_evento(dados)

@router.get("/eventos/{evento_id}", response_model=Evento)
def obter_evento(evento_id: int):
    evento = buscar_evento_por_id(evento_id)

    if evento is None:
        raise HTTPException(
            status_code=404,
            detail="Evento não encontrado."
        )

    return evento

@router.put("/eventos/{evento_id}", response_model=Evento)
def editar_evento(evento_id: int, dados: EventoEntrada):
    evento = atualizar_evento(evento_id, dados)

    if evento is None:
        raise HTTPException(
            status_code=404,
            detail="Evento não encontrado."
        )

    return evento

@router.delete("/eventos/{evento_id}", status_code=204)
def remover_evento(evento_id: int):
    removido = excluir_evento(evento_id)

    if not removido:
        raise HTTPException(
            status_code=404,
            detail="Evento não encontrado."
        )
