from datetime import date, time
from sqlalchemy import CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.db import Base

class Evento(Base):
    __tablename__ = "eventos"
    __table_args__ = (CheckConstraint("capacidade > 0", name="ck_evento_capacidade"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str]
    descricao: Mapped[str]
    data: Mapped[date]
    horario: Mapped[time]
    local: Mapped[str]
    capacidade: Mapped[int]
    categoria: Mapped[str]
    inscricoes: Mapped[list["Inscricao"]] = relationship(back_populates="evento", cascade="all, delete-orphan", passive_deletes=True)
