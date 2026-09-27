from app.models.inscricao_model import Inscricao
from app.models.participante_model import Participante
from app.repositories.inscricao_repository import InscricaoRepository
from app.services.erros import RegraNegocioError
from app.services.evento_service import EventoService
from app.services.participante_service import ParticipanteService


class InscricaoService:
    def __init__(
        self,
        repository: InscricaoRepository,
        eventos: EventoService,
        participantes: ParticipanteService,
    ):
        self.repository = repository
        self.eventos = eventos
        self.participantes = participantes

    def criar(self, evento_id: int, participante_id: int) -> Inscricao:
        evento = self.eventos.buscar(evento_id)
        self.participantes.buscar(participante_id)
        if self.repository.existe(evento_id, participante_id):
            raise RegraNegocioError("Participante já está inscrito neste evento.")
        if len(self.repository.listar_por_evento(evento_id)) >= evento.capacidade:
            raise RegraNegocioError("Não existem vagas disponíveis para este evento.")
        return self.repository.criar(evento_id, participante_id)

    def listar(self, evento_id: int) -> list[Participante]:
        self.eventos.buscar(evento_id)
        return [
            self.participantes.buscar(inscricao.participante_id)
            for inscricao in self.repository.listar_por_evento(evento_id)
        ]
