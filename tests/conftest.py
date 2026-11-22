import secrets

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text

from app.main import criar_app
from database.db import criar_engine


@pytest.fixture
def engine(tmp_path):
    banco = criar_engine(f"sqlite:///{(tmp_path / 'teste.db').as_posix()}")
    try:
        yield banco
    finally:
        banco.dispose()


@pytest.fixture
def cliente(engine, monkeypatch):
    monkeypatch.setenv("JWT_SECRET", secrets.token_urlsafe(48))
    with TestClient(criar_app(engine)) as cliente:
        yield cliente


@pytest.fixture
def evento():
    return dict(titulo="Oficina", descricao="Introdução", data="2027-04-12",
                horario="09:00:00", local="Sala 1", capacidade=2, categoria="Extensão")


@pytest.fixture
def participante():
    return dict(nome="Ana", email="ana@example.com", curso="Computação")


@pytest.fixture
def usuario():
    return dict(nome="Bia", email="bia@example.com", senha="Senha-de-teste#123")


@pytest.fixture
def autenticar(cliente, engine, usuario):
    def entrar(admin=False):
        resposta = cliente.post("/usuarios", json=usuario)
        assert resposta.status_code == 201, resposta.text
        if admin:
            with engine.begin() as conexao:
                conexao.execute(text("UPDATE usuarios SET perfil='administrador' WHERE email=:email"),
                                {"email": usuario["email"]})
        login = cliente.post("/auth/login", json={k: usuario[k] for k in ("email", "senha")})
        assert login.status_code == 200, login.text
        dados = login.json()
        assert dados["token_type"].lower() == "bearer"
        return {"Authorization": f"Bearer {dados['access_token']}"}

    return entrar
