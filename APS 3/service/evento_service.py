from schema.evento_schema import Evento, EventoEntrada
from sqlalchemy.orm import Session
from model import Evento as EventoDB
from sqlalchemy import select

eventos = []



def cadastrar_evento(dados: EventoEntrada, db: Session):
    novo_evento = EventoDB(
        **dados.model_dump()
    )

    db.add(novo_evento)
    db.commit()
    db.refresh(novo_evento)

    return novo_evento


def listar_eventos(db: Session):
    consulta = select(EventoDB).order_by(EventoDB.id)

    resultado = db.scalars(consulta).all()

    return resultado

def buscar_evento_por_id(evento_id: int, db: Session):
    return db.get(EventoDB, evento_id)


def atualizar_evento(evento_id: int, dados: EventoEntrada, db: Session):
    evento = db.get(EventoDB, evento_id)

    if evento is None:
        return None

    for campo, valor in dados.model_dump().items():
        setattr(evento, campo, valor)

    db.commit()
    db.refresh(evento)

    return evento

def excluir_evento(evento_id: int, db: Session):
    evento = db.get(EventoDB, evento_id)

    if evento is None:
        return False

    db.delete(evento)
    db.commit()

    return True
