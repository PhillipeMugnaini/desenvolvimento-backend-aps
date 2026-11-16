from service.evento_service import buscar_evento_por_id
from service.participante_service import buscar_participante_por_id


inscricoes = []

def inscrever_participante(evento_id: int, participante_id: int):
    evento = buscar_evento_por_id(evento_id)
    participante = buscar_participante_por_id(participante_id)

    if evento is None:
        return {"erro": "evento_nao_encontrado"}

    if participante is None:
        return {"erro": "participante_nao_encontrado"}

    for inscricao in inscricoes:
        if (
            inscricao["evento_id"] == evento_id
            and inscricao["participante_id"] == participante_id
        ):
            return {"erro": "participante_ja_inscrito"}

    total_inscritos = sum(
        1 for inscricao in inscricoes
        if inscricao["evento_id"] == evento_id
    )

    if total_inscritos >= evento.capacidade:
        return {"erro": "evento_sem_vagas"}

    nova_inscricao = {
        "evento_id": evento_id,
        "participante_id": participante_id
    }

    inscricoes.append(nova_inscricao)

    return nova_inscricao

def listar_inscritos(evento_id: int):
    participantes_inscritos = []

    for inscricao in inscricoes:
        if inscricao["evento_id"] == evento_id:
            participante = buscar_participante_por_id(
                inscricao["participante_id"]
            )

            if participante is not None:
                participantes_inscritos.append(participante)

    return participantes_inscritos