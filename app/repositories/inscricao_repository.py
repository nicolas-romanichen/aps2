from sqlalchemy import delete, select
from sqlalchemy.orm import joinedload
from app.models.inscricao_model import Inscricao

class InscricaoRepository:
    def __init__(self, session):
        self.session = session

    def criar(self, evento_id, participante_id):
        registro = Inscricao(evento_id=evento_id, participante_id=participante_id)
        self.session.add(registro)
        self.session.flush()
        return registro

    def existe(self, evento_id, participante_id):
        return self.session.scalar(select(Inscricao.id).where(Inscricao.evento_id == evento_id, Inscricao.participante_id == participante_id)) is not None

    def listar_por_evento(self, evento_id):
        return list(self.session.scalars(select(Inscricao).where(Inscricao.evento_id == evento_id).order_by(Inscricao.id)))

    def listar_participantes(self, evento_id):
        registros = self.session.scalars(select(Inscricao).options(joinedload(Inscricao.participante)).where(Inscricao.evento_id == evento_id).order_by(Inscricao.participante_id))
        return [registro.participante for registro in registros]

    def remover_por_evento(self, evento_id):
        self.session.execute(delete(Inscricao).where(Inscricao.evento_id == evento_id))

    def remover_por_participante(self, participante_id):
        self.session.execute(delete(Inscricao).where(Inscricao.participante_id == participante_id))
