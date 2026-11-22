import os
from datetime import datetime, timedelta, timezone

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


hasher = PasswordHasher()


def carregar_chave():
    chave = os.environ.get("JWT_SECRET", "")
    if len(chave.encode()) < 32:
        raise RuntimeError("Configure JWT_SECRET com ao menos 32 bytes antes de iniciar a API.")
    return chave


def conferir_senha(senha, senha_hash):
    try:
        return hasher.verify(senha_hash, senha)
    except VerifyMismatchError:
        return False


def emitir_token(usuario_id, chave):
    agora = datetime.now(timezone.utc)
    dados = {"sub": str(usuario_id), "iat": agora, "exp": agora + timedelta(minutes=30)}
    return jwt.encode(dados, chave, algorithm="HS256")


def identificar_token(token, chave):
    dados = jwt.decode(token, chave, algorithms=["HS256"], options={"require": ["sub", "exp"]})
    return int(dados["sub"])
