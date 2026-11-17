from schema.participante_schema import Participante, ParticipanteEntrada
from model import Participante as ParticipanteDB
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from model import Participante as ParticipanteDB

class EmailDuplicadoError(Exception):
    pass

participantes = []



def cadastrar_participante(dados: ParticipanteEntrada, db: Session):
    consulta = select(ParticipanteDB).where(
        ParticipanteDB.email == dados.email
    )

    participante_existente = db.scalar(consulta)

    if participante_existente is not None:
        return None

    novo_participante = ParticipanteDB(
        **dados.model_dump()
    )

    try:
        db.add(novo_participante)
        db.commit()

    except IntegrityError:
        db.rollback()
        return None

    db.refresh(novo_participante)

    return novo_participante

def listar_participantes(db: Session):
    consulta = select(ParticipanteDB).order_by(ParticipanteDB.id)

    participantes = db.scalars(consulta).all()

    return participantes

def buscar_participante_por_id(participante_id: int, db: Session):
    return db.get(ParticipanteDB, participante_id)


def atualizar_participante(
    participante_id: int,
    dados: ParticipanteEntrada,
    db: Session
):
    participante = db.get(ParticipanteDB, participante_id)

    if participante is None:
        return None

    consulta = select(ParticipanteDB).where(
        ParticipanteDB.email == dados.email,
        ParticipanteDB.id != participante_id
    )

    if db.scalar(consulta) is not None:
        raise EmailDuplicadoError()

    for campo, valor in dados.model_dump().items():
        setattr(participante, campo, valor)

    try:
        db.commit()
    except IntegrityError as erro:
        db.rollback()
        raise EmailDuplicadoError() from erro

    db.refresh(participante)

    return participante


def excluir_participante(participante_id: int, db: Session):
    participante = db.get(ParticipanteDB, participante_id)

    if participante is None:
        return False

    db.delete(participante)
    db.commit()

    return True
