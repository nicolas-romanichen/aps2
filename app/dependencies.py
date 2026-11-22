from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer
from jwt import InvalidTokenError
from app.repositories.usuario_repository import UsuarioRepository
from app.services.usuario_service import UsuarioService
from app.security import identificar_token
from database.db import get_db
from app.repositories.evento_repository import EventoRepository
from app.repositories.inscricao_repository import InscricaoRepository
from app.repositories.participante_repository import ParticipanteRepository
from app.services.evento_service import EventoService
from app.services.inscricao_service import InscricaoService
from app.services.participante_service import ParticipanteService
from app.repositories.relatorio_repository import RelatorioRepository
from app.services.relatorio_service import RelatorioService

def get_evento_service(session=Depends(get_db, scope="function")):
    return EventoService(EventoRepository(session), InscricaoRepository(session))

def get_participante_service(session=Depends(get_db, scope="function")):
    return ParticipanteService(ParticipanteRepository(session), InscricaoRepository(session))

def get_inscricao_service(session=Depends(get_db, scope="function")):
    return InscricaoService(InscricaoRepository(session), get_evento_service(session), get_participante_service(session))


def get_relatorio_service(session=Depends(get_db, scope="function")):
    return RelatorioService(RelatorioRepository(session))


def get_usuario_service(session=Depends(get_db, scope="function")):
    return UsuarioService(UsuarioRepository(session))


bearer = HTTPBearer(auto_error=False, bearerFormat="JWT")


def usuario_atual(request: Request, credencial=Depends(bearer), session=Depends(get_db, scope="function")):
    erro = HTTPException(401, "Não foi possível validar as credenciais.", headers={"WWW-Authenticate": "Bearer"})
    if credencial is None:
        raise erro
    try:
        usuario_id = identificar_token(credencial.credentials, request.app.state.chave)
    except (InvalidTokenError, ValueError):
        raise erro from None
    usuario = UsuarioRepository(session).buscar(usuario_id)
    if usuario is None:
        raise erro
    return usuario


def administrador(usuario=Depends(usuario_atual)):
    if usuario.perfil != "administrador":
        raise HTTPException(403, "Permissão de administrador necessária.")
    return usuario
