from service.evento_service import buscar_evento_por_id
from service.participante_service import buscar_participante_por_id
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from model import Evento, Participante, Inscricao


inscricoes = []


def inscrever_participante(
    evento_id: int,
    participante_id: int,
    db: Session
):
    # 1. Verificar se o evento existe
    evento = db.get(Evento, evento_id)

    if evento is None:
        return {"erro": "evento_nao_encontrado"}

    # 2. Verificar se o participante existe
    participante = db.get(Participante, participante_id)

    if participante is None:
        return {"erro": "participante_nao_encontrado"}

    # 3. Verificar se já está inscrito
    consulta = select(Inscricao.id).where(
        Inscricao.evento_id == evento_id,
        Inscricao.participante_id == participante_id
    )

    if db.scalar(consulta) is not None:
        return {"erro": "participante_ja_inscrito"}

    # 4. Contar quantas inscrições existem
    consulta_total = select(func.count(Inscricao.id)).where(
        Inscricao.evento_id == evento_id
    )

    total_inscritos = db.scalar(consulta_total) or 0

    # 5. Verificar disponibilidade de vagas
    if total_inscritos >= evento.capacidade:
        return {"erro": "evento_sem_vagas"}

    # 6. Criar a inscrição
    nova_inscricao = Inscricao(
        evento_id=evento_id,
        participante_id=participante_id
    )

    try:
        db.add(nova_inscricao)
        db.commit()

    except IntegrityError:
        db.rollback()
        return {"erro": "conflito_integridade"}

    db.refresh(nova_inscricao)

    return nova_inscricao


def listar_inscritos(evento_id: int, db: Session):
    # Verificar se o evento existe
    evento = db.get(Evento, evento_id)

    if evento is None:
        return None

    # Buscar participantes inscritos no evento
    consulta = (
        select(Participante)
        .join(
            Inscricao,
            Inscricao.participante_id == Participante.id
        )
        .where(Inscricao.evento_id == evento_id)
        .order_by(Participante.id)
    )

    participantes = db.scalars(consulta).all()

    return participantes
