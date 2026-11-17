from fastapi import APIRouter, HTTPException, Depends
from schema.evento_schema import Evento, EventoEntrada
from sqlalchemy.orm import Session
from database import get_db
from service.evento_service import (
    cadastrar_evento,
    listar_eventos,
    buscar_evento_por_id,
    atualizar_evento,
    excluir_evento,
    CapacidadeInsuficienteError
)


router = APIRouter()


@router.post("/eventos", response_model=Evento, status_code=201)
def criar_evento(
    dados: EventoEntrada,
    db: Session = Depends(get_db)
):
    return cadastrar_evento(dados, db)

@router.get("/eventos", response_model=list[Evento])
def obter_eventos(db: Session = Depends(get_db)):
    return listar_eventos(db)


@router.get("/eventos/{evento_id}", response_model=Evento)
def obter_evento(
    evento_id: int,
    db: Session = Depends(get_db)
):
    evento = buscar_evento_por_id(evento_id, db)

    if evento is None:
        raise HTTPException(
            status_code=404,
            detail="Evento não encontrado."
        )

    return evento

@router.put("/eventos/{evento_id}", response_model=Evento)
def editar_evento(
    evento_id: int,
    dados: EventoEntrada,
    db: Session = Depends(get_db)
):
    try:
        evento = atualizar_evento(evento_id, dados, db)

    except CapacidadeInsuficienteError:
        raise HTTPException(
            status_code=409,
            detail="A capacidade não pode ser menor que o número de inscritos."
        )

    if evento is None:
        raise HTTPException(
            status_code=404,
            detail="Evento não encontrado."
        )

    return evento



@router.delete("/eventos/{evento_id}", status_code=204)
def remover_evento(
    evento_id: int,
    db: Session = Depends(get_db)
):
    removido = excluir_evento(evento_id, db)

    if not removido:
        raise HTTPException(
            status_code=404,
            detail="Evento não encontrado."
        )
