from app.schemas.participante_schema import Participante, ParticipanteEntrada
from app.repositories.inscricao_repository import InscricaoRepository
from app.repositories.participante_repository import ParticipanteRepository
from app.services.erros import NaoEncontradoError, RegraNegocioError


class ParticipanteService:
    def __init__(self, repository: ParticipanteRepository, inscricoes: InscricaoRepository):
        self.repository = repository
        self.inscricoes = inscricoes

    def criar(self, dados: ParticipanteEntrada) -> Participante:
        self._validar_email(dados.email)
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
        self._validar_email(dados.email, participante_id)
        return self.repository.atualizar(participante_id, dados)

    def remover(self, participante_id: int) -> None:
        self.buscar(participante_id)
        self.inscricoes.remover_por_participante(participante_id)
        self.repository.remover(participante_id)

    def _validar_email(self, email, participante_id=None):
        existente = self.repository.buscar_por_email(email)
        if existente is not None and existente.id != participante_id:
            raise RegraNegocioError("Já existe um participante cadastrado com este e-mail.")
