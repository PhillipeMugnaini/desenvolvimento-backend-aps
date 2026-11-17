
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from model import Evento, Inscricao, Participante

def relatorio_ocupacao(db: Session):
    consulta = (
        select(
            Evento.id.label("evento_id"),
            Evento.titulo,
            Evento.capacidade,
            func.count(Inscricao.id).label("total_inscritos")
        )
        .outerjoin(
            Inscricao,
            Inscricao.evento_id == Evento.id
        )
        .group_by(
            Evento.id,
            Evento.titulo,
            Evento.capacidade
        )
        .order_by(Evento.id)
    )

    resultados = db.execute(consulta).all()

    relatorio = []

    for resultado in resultados:
        capacidade = resultado.capacidade
        inscritos = resultado.total_inscritos

        vagas = capacidade - inscritos

        percentual = (
            round((inscritos / capacidade) * 100, 2)
            if capacidade > 0
            else 0.0
        )

        relatorio.append({
            "evento_id": resultado.evento_id,
            "titulo": resultado.titulo,
            "capacidade": capacidade,
            "total_inscritos": inscritos,
            "vagas_disponiveis": vagas,
            "percentual_ocupacao": percentual
        })

    return relatorio


def relatorio_categorias(db: Session):

    # 1. Contar inscrições de cada evento
    subconsulta = (
        select(
            Inscricao.evento_id,
            func.count(Inscricao.id).label("total_inscricoes")
        )
        .group_by(Inscricao.evento_id)
        .subquery()
    )

    # 2. Agrupar os eventos por categoria
    consulta = (
        select(
            Evento.categoria,
            func.count(Evento.id).label("total_eventos"),
            func.sum(Evento.capacidade).label("capacidade_total"),
            func.coalesce(
                func.sum(subconsulta.c.total_inscricoes), 0
            ).label("total_inscricoes")
        )
        .outerjoin(
            subconsulta,
            Evento.id == subconsulta.c.evento_id
        )
        .group_by(Evento.categoria)
        .order_by(Evento.categoria)
    )

    # 3. Executar a consulta
    resultados = db.execute(consulta).mappings().all()

    # 4. Retornar os resultados
    return [dict(resultado) for resultado in resultados]

def relatorio_cursos(db: Session):

    # 1. Contar as inscrições de cada participante
    subconsulta = (
        select(
            Inscricao.participante_id,
            func.count(Inscricao.id).label("total_inscricoes")
        )
        .group_by(Inscricao.participante_id)
        .subquery()
    )

    # 2. Agrupar os participantes por curso
    consulta = (
        select(
            Participante.curso,
            func.count(Participante.id).label("total_participantes"),
            func.coalesce(
                func.sum(subconsulta.c.total_inscricoes), 0
            ).label("total_inscricoes")
        )
        .outerjoin(
            subconsulta,
            Participante.id == subconsulta.c.participante_id
        )
        .group_by(Participante.curso)
        .order_by(Participante.curso)
    )

    # 3. Executar a consulta
    resultados = db.execute(consulta).mappings().all()

    # 4. Retornar o relatório
    return [dict(resultado) for resultado in resultados]
