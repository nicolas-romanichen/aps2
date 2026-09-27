from app.models.participante_model import Participante, ParticipanteEntrada

class ParticipanteRepository:
    def __init__(self):
        self._participantes: dict[int, Participante] = {}
        self._proximo_id = 1

    def criar(self, dados: ParticipanteEntrada) -> Participante:
        participante = Participante(id=self._proximo_id, **dados.model_dump())
        self._participantes[participante.id] = participante
        self._proximo_id += 1
        return participante

    def listar(self) -> list[Participante]:
        return list(self._participantes.values())

    def buscar(self, participante_id: int) -> Participante | None:
        return self._participantes.get(participante_id)

    def atualizar(self, participante_id: int, dados: ParticipanteEntrada) -> Participante:
        participante = Participante(id=participante_id, **dados.model_dump())
        self._participantes[participante_id] = participante
        return participante

    def remover(self, participante_id: int) -> None:
        self._participantes.pop(participante_id, None)
