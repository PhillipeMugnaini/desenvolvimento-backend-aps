
import os

from pathlib import Path
from datetime import datetime, timedelta, timezone

import jwt

from dotenv import load_dotenv
from jwt.exceptions import InvalidTokenError


# Carregar as variáveis do arquivo .env
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

CHAVE_SECRETA = os.getenv("JWT_SECRET_KEY")

ALGORITMO = "HS256"
TEMPO_EXPIRACAO = 30


if not CHAVE_SECRETA or len(CHAVE_SECRETA) < 32:
    raise RuntimeError(
        "JWT_SECRET_KEY não configurada corretamente."
    )


def gerar_token(usuario_id: int) -> str:
    agora = datetime.now(timezone.utc)

    dados = {
        "sub": str(usuario_id),
        "iat": agora,
        "exp": agora + timedelta(
            minutes=TEMPO_EXPIRACAO
        )
    }

    return jwt.encode(
        dados,
        CHAVE_SECRETA,
        algorithm=ALGORITMO
    )


def validar_token(token: str) -> int:
    dados = jwt.decode(
        token,
        CHAVE_SECRETA,
        algorithms=[ALGORITMO],
        options={
            "require": ["sub", "iat", "exp"]
        }
    )

    usuario_id = dados["sub"]

    if (
        not isinstance(usuario_id, str)
        or not usuario_id.isdecimal()
        or int(usuario_id) < 1
    ):
        raise InvalidTokenError(
            "Identificador de usuário inválido."
        )

    return int(usuario_id)
