
from sqlalchemy import select
from sqlalchemy.orm import Session

from model import Usuario
from security.password import verificar_senha
from security.jwt import gerar_token


def autenticar_usuario(
    email: str,
    senha: str,
    db: Session
):
    # 1. Normalizar o e-mail
    email = email.strip().lower()

    # 2. Consultar o usuário no banco
    consulta = select(Usuario).where(
        Usuario.email == email
    )

    usuario = db.scalar(consulta)

    # 3. Verificar se o usuário existe
    if usuario is None:
        return None

    # 4. Verificar a senha
    if not verificar_senha(senha, usuario.senha_hash):
        return None

    # 5. Gerar o token JWT
    token = gerar_token(usuario.id)

    return token
