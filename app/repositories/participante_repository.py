from app.models.participante_model import Participante
from app.repositories.base_repository import BaseRepository

class ParticipanteRepository(BaseRepository):
    model = Participante

    def buscar_por_email(self, email):
        from sqlalchemy import select
        return self.session.scalar(select(self.model).where(self.model.email == email))
