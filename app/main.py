from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.routers import evento_router, inscricao_router, participante_router
from app.services.erros import NaoEncontradoError, RegraNegocioError


app = FastAPI(title="APS 2 — Eventos acadêmicos")


@app.exception_handler(NaoEncontradoError)
async def tratar_nao_encontrado(request: Request, erro: NaoEncontradoError):
    return JSONResponse(status_code=404, content={"detail": str(erro)})


@app.exception_handler(RegraNegocioError)
async def tratar_regra_negocio(request: Request, erro: RegraNegocioError):
    return JSONResponse(status_code=400, content={"detail": str(erro)})


app.include_router(evento_router.router)
app.include_router(participante_router.router)
app.include_router(inscricao_router.router)
