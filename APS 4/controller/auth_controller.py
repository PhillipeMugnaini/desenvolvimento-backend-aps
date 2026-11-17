
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from schema.auth_schema import LoginEntrada, TokenSaida
from service.auth_service import autenticar_usuario


router = APIRouter(
    prefix="/auth",
    tags=["Autenticação"]
)


@router.post("/login", response_model=TokenSaida)
def login(
    dados: LoginEntrada,
    db: Session = Depends(get_db)
):
    token = autenticar_usuario(
        email=str(dados.email),
        senha=dados.senha,
        db=db
    )

    if token is None:
        raise HTTPException(
            status_code=401,
            detail="E-mail ou senha inválidos.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return {
        "access_token": token,
        "token_type": "bearer"
    }
