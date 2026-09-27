from app.models.evento_model import Evento, EventoEntrada
from app.repositories.evento_repository import EventoRepository
from app.repositories.inscricao_repository import InscricaoRepository
from app.services.erros import NaoEncontradoError, RegraNegocioError


class EventoService:
    def __init__(self, repository: EventoRepository, inscricoes: InscricaoRepository):
        self.repository = repository
        self.inscricoes = inscricoes

    def criar(self, dados: EventoEntrada) -> Evento:
        return self.repository.criar(dados)

    def listar(self) -> list[Evento]:
        return self.repository.listar()

    def buscar(self, evento_id: int) -> Evento:
        evento = self.repository.buscar(evento_id)
        if evento is None:
            raise NaoEncontradoError("Evento não encontrado.")
        return evento

    def atualizar(self, evento_id: int, dados: EventoEntrada) -> Evento:
        self.buscar(evento_id)
        if dados.capacidade < len(self.inscricoes.listar_por_evento(evento_id)):
            raise RegraNegocioError("A capacidade não pode ser menor que o número de inscritos.")
        return self.repository.atualizar(evento_id, dados)

    def remover(self, evento_id: int) -> None:
        self.buscar(evento_id)
        self.inscricoes.remover_por_evento(evento_id)
        self.repository.remover(evento_id)
