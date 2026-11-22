from sqlalchemy import CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from database.db import Base


class Usuario(Base):
    __tablename__ = "usuarios"
    __table_args__ = (CheckConstraint("perfil IN ('usuario', 'administrador')"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    senha_hash: Mapped[str]
    perfil: Mapped[str] = mapped_column(default="usuario")
