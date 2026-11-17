
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from model import Usuario
from schema.usuario_schema import UsuarioCriacao
from security.password import gerar_hash


class EmailUsuarioDuplicadoError(Exception):
    pass


def cadastrar_usuario(dados: UsuarioCriacao, db: Session):

    # 1. Normalizar o e-mail
    email = str(dados.email).strip().lower()

    # 2. Verificar se o e-mail já está cadastrado
    consulta = select(Usuario.id).where(
        func.lower(Usuario.email) == email
    )

    usuario_existente = db.scalar(consulta)

    if usuario_existente is not None:
        raise EmailUsuarioDuplicadoError()

    # 3. Gerar o hash da senha
    senha_protegida = gerar_hash(dados.senha)

    # 4. Criar o usuário com perfil comum
    novo_usuario = Usuario(
        nome=dados.nome,
        email=email,
        senha_hash=senha_protegida,
        perfil="usuario"
    )

    # 5. Salvar no banco de dados
    try:
        db.add(novo_usuario)
        db.commit()

    except IntegrityError as erro:
        db.rollback()
        raise EmailUsuarioDuplicadoError() from erro

    # 6. Atualizar o objeto
    db.refresh(novo_usuario)

    return novo_usuario
