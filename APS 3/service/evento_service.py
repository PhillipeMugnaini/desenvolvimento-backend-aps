from model.evento import Evento, EventoEntrada


eventos = []


def cadastrar_evento(dados: EventoEntrada):
    novo_evento = Evento(
        id=len(eventos) + 1,
        **dados.model_dump()
    )

    eventos.append(novo_evento)

    return novo_evento

def listar_eventos():
    return eventos

def buscar_evento_por_id(evento_id: int):
    for evento in eventos:
        if evento.id == evento_id:
            return evento

    return None

def atualizar_evento(evento_id: int, dados: EventoEntrada):
    for indice, evento in enumerate(eventos):
        if evento.id == evento_id:
            evento_atualizado = Evento(
                id=evento_id,
                **dados.model_dump()
            )

            eventos[indice] = evento_atualizado

            return evento_atualizado

    return None

def excluir_evento(evento_id: int):
    for indice, evento in enumerate(eventos):
        if evento.id == evento_id:
            eventos.pop(indice)
            return True

    return False