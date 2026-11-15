from pathlib import Path

from fastapi import Request
from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_PATH = Path(__file__).resolve().parents[1] / "database.db"

class Base(DeclarativeBase):
    pass

def criar_engine(url):
    engine = create_engine(url, connect_args={"check_same_thread": False, "timeout": 30})
    @event.listens_for(engine, "connect")
    def configurar_sqlite(conexao, _):
        cursor = conexao.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
    return engine

db = criar_engine(f"sqlite:///{DATABASE_PATH.as_posix()}")
Session = sessionmaker(bind=db, expire_on_commit=False)

def criar_tabelas(engine):
    from app.models import evento_model, participante_model, inscricao_model
    Base.metadata.create_all(engine)

def get_db(request: Request):
    with request.app.state.session_factory() as session:
        try:
            # Reserva a escrita antes de verificar vagas, inclusive entre processos.
            if request.method in {"POST", "PUT", "DELETE", "PATCH"}:
                session.execute(text("BEGIN IMMEDIATE"))
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
