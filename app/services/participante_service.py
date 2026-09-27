from app.models.participante_model import Participante, ParticipanteEntrada
from app.repositories.inscricao_repository import InscricaoRepository
from app.repositories.participante_repository import ParticipanteRepository
from app.services.erros import NaoEncontradoError


class ParticipanteService:
    def __init__(self, repository: ParticipanteRepository, inscricoes: InscricaoRepository):
        self.repository = repository
        self.inscricoes = inscricoes

    def criar(self, dados: ParticipanteEntrada) -> Participante:
        return self.repository.criar(dados)

    def listar(self) -> list[Participante]:
        return self.repository.listar()

    def buscar(self, participante_id: int) -> Participante:
        participante = self.repository.buscar(participante_id)
        if participante is None:
            raise NaoEncontradoError("Participante não encontrado.")
        return participante

    def atualizar(self, participante_id: int, dados: ParticipanteEntrada) -> Participante:
        self.buscar(participante_id)
        return self.repository.atualizar(participante_id, dados)

    def remover(self, participante_id: int) -> None:
        self.buscar(participante_id)
        self.inscricoes.remover_por_participante(participante_id)
        self.repository.remover(participante_id)
