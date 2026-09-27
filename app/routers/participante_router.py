from fastapi import APIRouter

from app.dependencies import participante_service
from app.models.participante_model import Participante, ParticipanteEntrada


router = APIRouter(prefix="/participantes", tags=["Participantes"])

@router.post("", response_model=Participante, status_code=201)
async def criar_participante(dados: ParticipanteEntrada):
    return participante_service.criar(dados)

@router.get("", response_model=list[Participante])
async def listar_participantes():
    return participante_service.listar()

@router.get("/{id}", response_model=Participante)
async def buscar_participante(id: int):
    return participante_service.buscar(id)

@router.put("/{id}", response_model=Participante)
async def atualizar_participante(id: int, dados: ParticipanteEntrada):
    return participante_service.atualizar(id, dados)

@router.delete("/{id}", status_code=200)
async def remover_participante(id: int):
    participante_service.remover(id)
    return {
        "codigo": 200,
        "mensagem": f"Participante {id} removido com sucesso"
    }