from fastapi import APIRouter, Depends

from app.dependencies import get_participante_service
from app.schemas.participante_schema import Participante, ParticipanteEntrada


router = APIRouter(prefix="/participantes", tags=["Participantes"])

@router.post("", response_model=Participante, status_code=201)
def criar_participante(dados: ParticipanteEntrada, participante_service=Depends(get_participante_service)):
    return participante_service.criar(dados)

@router.get("", response_model=list[Participante])
def listar_participantes(participante_service=Depends(get_participante_service)):
    return participante_service.listar()

@router.get("/{id}", response_model=Participante)
def buscar_participante(id: int, participante_service=Depends(get_participante_service)):
    return participante_service.buscar(id)

@router.put("/{id}", response_model=Participante)
def atualizar_participante(id: int, dados: ParticipanteEntrada, participante_service=Depends(get_participante_service)):
    return participante_service.atualizar(id, dados)

@router.delete("/{id}", status_code=200)
def remover_participante(id: int, participante_service=Depends(get_participante_service)):
    participante_service.remover(id)
    return {
        "codigo": 200,
        "mensagem": f"Participante {id} removido com sucesso"
    }