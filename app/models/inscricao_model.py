from datetime import date, datetime
from zoneinfo import ZoneInfo
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.db import Base

def data_atual():
    return datetime.now(ZoneInfo("America/Sao_Paulo")).date()

class Inscricao(Base):
    __tablename__ = "inscricoes"
    __table_args__ = (UniqueConstraint("evento_id", "participante_id", name="uq_inscricao"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    evento_id: Mapped[int] = mapped_column(ForeignKey("eventos.id", ondelete="CASCADE"), index=True)
    participante_id: Mapped[int] = mapped_column(ForeignKey("participantes.id", ondelete="CASCADE"), index=True)
    data_inscricao: Mapped[date] = mapped_column(default=data_atual)
    evento: Mapped["Evento"] = relationship(back_populates="inscricoes")
    participante: Mapped["Participante"] = relationship(back_populates="inscricoes")
