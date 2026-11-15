from sqlalchemy import select, func, case
from app.models.evento_model import Evento
from app.models.participante_model import Participante
from app.models.inscricao_model import Inscricao

class RelatorioRepository:
    def __init__(self, session):
        self.session = session

    def _inscricoes_por_evento(self):
        return select(Inscricao.evento_id, func.count(Inscricao.id).label("total")).group_by(Inscricao.evento_id).subquery()

    def ocupacao(self):
        contagem = self._inscricoes_por_evento()
        total = func.coalesce(contagem.c.total, 0)
        percentual = case((Evento.capacidade > 0, total * 100.0 / Evento.capacidade), else_=0.0)
        consulta = select(
            Evento.id.label("evento_id"), Evento.titulo, Evento.capacidade,
            total.label("total_inscritos"),
            (Evento.capacidade - total).label("vagas_disponiveis"),
            func.round(percentual, 2).label("percentual_ocupacao"),
        ).outerjoin(contagem, contagem.c.evento_id == Evento.id).order_by(Evento.id)
        return self.session.execute(consulta).mappings().all()

    def categorias(self):
        contagem = self._inscricoes_por_evento()
        consulta = select(
            Evento.categoria, func.count(Evento.id).label("total_eventos"),
            func.sum(Evento.capacidade).label("capacidade_total"),
            func.sum(func.coalesce(contagem.c.total, 0)).label("total_inscricoes"),
        ).outerjoin(contagem, contagem.c.evento_id == Evento.id).group_by(Evento.categoria).order_by(Evento.categoria)
        return self.session.execute(consulta).mappings().all()

    def cursos(self):
        consulta = select(
            Participante.curso,
            func.count(func.distinct(Participante.id)).label("total_participantes"),
            func.count(Inscricao.id).label("total_inscricoes"),
        ).outerjoin(Inscricao, Inscricao.participante_id == Participante.id).group_by(Participante.curso).order_by(Participante.curso)
        return self.session.execute(consulta).mappings().all()
