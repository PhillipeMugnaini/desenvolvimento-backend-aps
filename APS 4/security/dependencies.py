
from fastapi import Depends, HTTPException, status
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)

from sqlalchemy.orm import Session
from jwt.exceptions import InvalidTokenError

from database import get_db
from model import Usuario
from security.jwt import validar_token


# Configuração para receber tokens Bearer
bearer_scheme = HTTPBearer(auto_error=False)


def obter_usuario_atual(
    credenciais: HTTPAuthorizationCredentials | None = Depends(
        bearer_scheme
    ),
    db: Session = Depends(get_db)
) -> Usuario:

    # Erro padrão de autenticação
    erro_autenticacao = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou ausente.",
        headers={"WWW-Authenticate": "Bearer"}
    )

    # 1. Verificar se o token foi enviado
    if credenciais is None:
        raise erro_autenticacao

    # 2. Validar o JWT e recuperar o ID
    try:
        usuario_id = validar_token(
            credenciais.credentials
        )
    except InvalidTokenError:
        raise erro_autenticacao from None

    # 3. Procurar o usuário no banco
    usuario = db.get(Usuario, usuario_id)

    # 4. Verificar se o usuário existe
    if usuario is None:
        raise erro_autenticacao

    # 5. Retornar o usuário autenticado
    return usuario
