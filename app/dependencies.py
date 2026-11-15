from fastapi import Depends
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
