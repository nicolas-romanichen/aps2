from fastapi import APIRouter, Depends

from app.dependencies import administrador, get_evento_service
from app.schemas.evento_schema import Evento, EventoEntrada


router = APIRouter(prefix="/eventos", tags=["Eventos"])

@router.post("", response_model=Evento, status_code=201, dependencies=[Depends(administrador)])
def criar_evento(dados: EventoEntrada, evento_service=Depends(get_evento_service)):
    return evento_service.criar(dados)

@router.get("", response_model=list[Evento])
def listar_eventos(evento_service=Depends(get_evento_service)):
    return evento_service.listar()

@router.get("/{id}", response_model=Evento)
def buscar_evento(id: int, evento_service=Depends(get_evento_service)):
    return evento_service.buscar(id)

@router.put("/{id}", response_model=Evento, dependencies=[Depends(administrador)])
def atualizar_evento(id: int, dados: EventoEntrada, evento_service=Depends(get_evento_service)):
    return evento_service.atualizar(id, dados)

@router.delete("/{id}", status_code=200, dependencies=[Depends(administrador)])
def remover_evento(id: int, evento_service=Depends(get_evento_service)):
    evento_service.remover(id)
    return {
        "codigo": 200,
        "mensagem": f"Evento {id} removido com sucesso"
    }

