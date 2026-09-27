from app.models.evento_model import Evento, EventoEntrada

class EventoRepository:
    def __init__(self):
        self._eventos: dict[int, Evento] = {}
        self._proximo_id = 1

    def criar(self, dados: EventoEntrada) -> Evento:
        evento = Evento(id=self._proximo_id, **dados.model_dump())
        self._eventos[evento.id] = evento
        self._proximo_id += 1
        return evento

    def listar(self) -> list[Evento]:
        return list(self._eventos.values())

    def buscar(self, evento_id: int) -> Evento | None:
        return self._eventos.get(evento_id)

    def atualizar(self, evento_id: int, dados: EventoEntrada) -> Evento:
        evento = Evento(id=evento_id, **dados.model_dump())
        self._eventos[evento_id] = evento
        return evento

    def remover(self, evento_id: int) -> None:
        self._eventos.pop(evento_id, None)
