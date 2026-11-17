
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from service.relatorio_service import (
    relatorio_ocupacao,
    relatorio_categorias,
    relatorio_cursos
)

router = APIRouter(
    prefix="/relatorios",
    tags=["Relatórios"]
)

@router.get("/eventos/ocupacao")
def obter_relatorio_ocupacao(
    db: Session = Depends(get_db)
):
    return relatorio_ocupacao(db)

@router.get("/eventos/categorias")
def obter_relatorio_categorias(
    db: Session = Depends(get_db)
):
    return relatorio_categorias(db)

@router.get("/participantes/cursos")
def obter_relatorio_cursos(
    db: Session = Depends(get_db)
):
    return relatorio_cursos(db)
