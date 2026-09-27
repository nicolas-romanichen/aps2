from fastapi import APIRouter

from app.dependencies import inscricao_service
from app.models.inscricao_model import Inscricao
from app.models.participante_model import Participante


router = APIRouter(prefix="/eventos/{evento_id}/inscricoes", tags=["Inscrições"])

@router.post("/{participante_id}", response_model=Inscricao, status_code=201)
async def criar_inscricao(evento_id: int, participante_id: int):
    return inscricao_service.criar(evento_id, participante_id)

@router.get("", response_model=list[Participante])
async def listar_inscritos(evento_id: int):
    return inscricao_service.listar(evento_id)
