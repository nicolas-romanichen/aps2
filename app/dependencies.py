from app.repositories.evento_repository import EventoRepository
from app.repositories.inscricao_repository import InscricaoRepository
from app.repositories.participante_repository import ParticipanteRepository
from app.services.evento_service import EventoService
from app.services.inscricao_service import InscricaoService
from app.services.participante_service import ParticipanteService


inscricao_repository = InscricaoRepository()
evento_service = EventoService(EventoRepository(), inscricao_repository)
participante_service = ParticipanteService(ParticipanteRepository(), inscricao_repository)
inscricao_service = InscricaoService(
    inscricao_repository, evento_service, participante_service
)
