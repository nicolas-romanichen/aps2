from fastapi import APIRouter, Depends
from app.dependencies import administrador, get_relatorio_service
from app.schemas.relatorio_schema import Ocupacao, Categoria, Curso

router = APIRouter(prefix="/relatorios", tags=["Relatórios"], dependencies=[Depends(administrador)])

@router.get("/eventos/ocupacao", response_model=list[Ocupacao])
def ocupacao(service=Depends(get_relatorio_service)):
    return service.ocupacao()

@router.get("/eventos/categorias", response_model=list[Categoria])
def categorias(service=Depends(get_relatorio_service)):
    return service.categorias()

@router.get("/participantes/cursos", response_model=list[Curso])
def cursos(service=Depends(get_relatorio_service)):
    return service.cursos()
