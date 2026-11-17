from schema.evento_schema import Evento, EventoEntrada
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from model import Evento as EventoDB
from model import Inscricao as InscricaoDB

class CapacidadeInsuficienteError(Exception):
    pass

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



def atualizar_evento(
    evento_id: int,
    dados: EventoEntrada,
    db: Session
):
    # 1. Buscar o evento no banco
    evento = db.get(EventoDB, evento_id)

    if evento is None:
        return None

    # 2. Contar os participantes inscritos
    consulta = select(func.count(InscricaoDB.id)).where(
        InscricaoDB.evento_id == evento_id
    )

    total_inscritos = db.scalar(consulta) or 0

    # 3. Verificar se a nova capacidade é suficiente
    if dados.capacidade < total_inscritos:
        raise CapacidadeInsuficienteError()

    # 4. Atualizar os dados do evento
    for campo, valor in dados.model_dump().items():
        setattr(evento, campo, valor)

    # 5. Salvar as alterações
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
