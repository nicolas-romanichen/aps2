from fastapi import APIRouter, Depends, HTTPException, Request

from app.dependencies import get_usuario_service, usuario_atual
from app.schemas.usuario_schema import Credenciais, Token, UsuarioEntrada, UsuarioPublico
from app.security import emitir_token


router = APIRouter(tags=["Usuários e autenticação"])


@router.post("/usuarios", status_code=201, response_model=UsuarioPublico)
def cadastrar_usuario(dados: UsuarioEntrada, service=Depends(get_usuario_service)):
    return service.criar(dados)


@router.post("/auth/login", response_model=Token)
def login(dados: Credenciais, request: Request, service=Depends(get_usuario_service)):
    usuario = service.autenticar(dados)
    if usuario is None:
        raise HTTPException(401, "E-mail ou senha inválidos.", headers={"WWW-Authenticate": "Bearer"})
    return Token(access_token=emitir_token(usuario.id, request.app.state.chave))


@router.get("/auth/me", response_model=UsuarioPublico)
def meu_perfil(usuario=Depends(usuario_atual)):
    return usuario
