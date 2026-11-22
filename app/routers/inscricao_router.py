from fastapi import APIRouter, Depends

from app.dependencies import usuario_atual, get_inscricao_service
from app.schemas.inscricao_schema import Inscricao
from app.schemas.participante_schema import Participante


router = APIRouter(prefix="/eventos/{evento_id}/inscricoes", tags=["Inscrições"], dependencies=[Depends(usuario_atual)])

@router.post("/{participante_id}", response_model=Inscricao, status_code=201)
def criar_inscricao(evento_id: int, participante_id: int, inscricao_service=Depends(get_inscricao_service)):
    return inscricao_service.criar(evento_id, participante_id)

@router.get("", response_model=list[Participante])
def listar_inscritos(evento_id: int, inscricao_service=Depends(get_inscricao_service)):
    return inscricao_service.listar(evento_id)
