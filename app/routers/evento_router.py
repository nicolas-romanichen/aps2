from fastapi import APIRouter, Response

from app.dependencies import evento_service
from app.models.evento_model import Evento, EventoEntrada


router = APIRouter(prefix="/eventos", tags=["Eventos"])

@router.post("", response_model=Evento, status_code=201)
async def criar_evento(dados: EventoEntrada):
    return evento_service.criar(dados)

@router.get("", response_model=list[Evento])
async def listar_eventos():
    return evento_service.listar()

@router.get("/{id}", response_model=Evento)
async def buscar_evento(id: int):
    return evento_service.buscar(id)

@router.put("/{id}", response_model=Evento)
async def atualizar_evento(id: int, dados: EventoEntrada):
    return evento_service.atualizar(id, dados)

@router.delete("/{id}", status_code=204)
async def remover_evento(id: int):
    evento_service.remover(id)
    return Response(status_code=204)
