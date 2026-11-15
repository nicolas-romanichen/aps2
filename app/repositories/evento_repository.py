from app.models.evento_model import Evento
from app.repositories.base_repository import BaseRepository

class EventoRepository(BaseRepository):
    model = Evento
