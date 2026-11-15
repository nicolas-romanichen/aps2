import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from database.db import db, criar_tabelas
from app.routers import evento_router, inscricao_router, participante_router, relatorio_router
from app.services.erros import NaoEncontradoError, RegraNegocioError

logger = logging.getLogger(__name__)

def criar_app(engine=None):
    engine = engine if engine is not None else db

    @asynccontextmanager
    async def lifespan(app):
        criar_tabelas(engine)
        yield

    app = FastAPI(title="APS 3 — Eventos acadêmicos", lifespan=lifespan)
    app.state.session_factory = sessionmaker(bind=engine, expire_on_commit=False)

    @app.exception_handler(NaoEncontradoError)
    async def tratar_nao_encontrado(request: Request, erro: NaoEncontradoError):
        return JSONResponse(status_code=404, content={"detail": str(erro)})

    @app.exception_handler(RegraNegocioError)
    async def tratar_regra_negocio(request: Request, erro: RegraNegocioError):
        return JSONResponse(status_code=409, content={"detail": str(erro)})

    @app.exception_handler(IntegrityError)
    async def tratar_integridade(request: Request, erro: IntegrityError):
        logger.exception("Falha de integridade no banco", exc_info=erro)
        mensagem = "A operação viola a integridade dos dados."
        detalhe = str(erro.orig)
        if "participantes.email" in detalhe:
            mensagem = "Já existe um participante cadastrado com este e-mail."
        elif "inscricoes.evento_id, inscricoes.participante_id" in detalhe:
            mensagem = "Participante já está inscrito neste evento."
        return JSONResponse(status_code=409, content={"detail": mensagem})

    @app.exception_handler(SQLAlchemyError)
    async def tratar_persistencia(request: Request, erro: SQLAlchemyError):
        logger.exception("Falha ao acessar banco de dados", exc_info=erro)
        return JSONResponse(status_code=500, content={"detail": "Não foi possível concluir a operação no banco de dados."})

    for router in (evento_router, participante_router, inscricao_router, relatorio_router):
        app.include_router(router.router)
    return app

app = criar_app()
