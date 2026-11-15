from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.db import Base

class Participante(Base):
    __tablename__ = "participantes"
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    curso: Mapped[str]
    inscricoes: Mapped[list["Inscricao"]] = relationship(back_populates="participante", cascade="all, delete-orphan", passive_deletes=True)
