from fastapi import FastAPI

from controller.evento_controller import router as evento_router
from controller.participante_controller import router as participante_router
from controller.inscricao_controller import router as inscricao_router


app = FastAPI()

app.include_router(evento_router)
app.include_router(participante_router)
app.include_router(inscricao_router)


@app.get("/")
def inicio():
    return {"mensagem": "API de Eventos Acadêmicos funcionando!"}