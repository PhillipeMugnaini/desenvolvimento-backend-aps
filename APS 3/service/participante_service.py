from model.participante import Participante, ParticipanteEntrada


participantes = []


def cadastrar_participante(dados: ParticipanteEntrada):
    novo_participante = Participante(
        id=len(participantes) + 1,
        **dados.model_dump()
    )

    participantes.append(novo_participante)

    return novo_participante

def listar_participantes():
    return participantes

def buscar_participante_por_id(participante_id: int):
    for participante in participantes:
        if participante.id == participante_id:
            return participante

    return None

def atualizar_participante(participante_id: int, dados: ParticipanteEntrada):
    for indice, participante in enumerate(participantes):
        if participante.id == participante_id:
            participante_atualizado = Participante(
                id=participante_id,
                **dados.model_dump()
            )

            participantes[indice] = participante_atualizado

            return participante_atualizado

    return None

def excluir_participante(participante_id: int):
    for indice, participante in enumerate(participantes):
        if participante.id == participante_id:
            participantes.pop(indice)
            return True

    return False