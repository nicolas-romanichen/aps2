import base64
import json
from datetime import datetime, timezone

import pytest
import time_machine
from sqlalchemy import text
from argon2 import PasswordHasher


def test_cadastro_e_armazenamento_da_senha(cliente, engine, usuario):
    resposta = cliente.post("/usuarios", json=usuario)
    assert resposta.status_code == 201, resposta.text
    publico = resposta.json()
    assert publico == dict(id=publico["id"], nome=usuario["nome"], email=usuario["email"], perfil="usuario")
    with engine.connect() as conexao:
        linha = conexao.execute(text("SELECT * FROM usuarios WHERE email=:email"), usuario).mappings().one()
    assert linha["senha_hash"].startswith("$argon2id$")
    assert PasswordHasher().verify(linha["senha_hash"], usuario["senha"])
    assert usuario["senha"] not in linha.values()


def test_usuario_duplicado(cliente, usuario):
    assert cliente.post("/usuarios", json=usuario).status_code == 201
    assert cliente.post("/usuarios", json=usuario).status_code == 409


def test_credenciais_invalidas(cliente, usuario):
    assert cliente.post("/usuarios", json=usuario).status_code == 201
    erros = []
    for email in (usuario["email"], "ausente@example.com"):
        resposta = cliente.post("/auth/login", json=dict(email=email, senha="Senha-errada#123"))
        assert resposta.status_code == 401
        erros.append(resposta.json()["detail"])
    assert erros[0] == erros[1]


def test_login_e_perfil(cliente, autenticar, usuario):
    resposta = cliente.get("/auth/me", headers=autenticar())
    assert resposta.status_code == 200
    perfil = resposta.json()
    assert perfil == dict(id=perfil["id"], nome=usuario["nome"], email=usuario["email"], perfil="usuario")


@pytest.mark.parametrize("metodo,rota,corpo", [
    ("POST", "/eventos", "evento"), ("PUT", "/eventos/1", "evento"), ("DELETE", "/eventos/1", None),
    ("POST", "/participantes", "participante"), ("PUT", "/participantes/1", "participante"),
    ("DELETE", "/participantes/1", None), ("POST", "/eventos/1/inscricoes/1", None),
    ("GET", "/relatorios/eventos/ocupacao", None), ("GET", "/relatorios/eventos/categorias", None),
    ("GET", "/relatorios/participantes/cursos", None), ("GET", "/auth/me", None),
])
def test_rota_exige_token(cliente, request, metodo, rota, corpo):
    dados = request.getfixturevalue(corpo) if corpo else None
    assert cliente.request(metodo, rota, json=dados).status_code == 401


def test_token_invalido(cliente):
    resposta = cliente.get("/relatorios/eventos/ocupacao", headers={"Authorization": "Bearer invalido"})
    assert resposta.status_code == 401


def test_token_expirado(cliente, autenticar):
    headers = autenticar()
    assert cliente.get("/auth/me", headers=headers).status_code == 200
    payload = headers["Authorization"].split(".")[1]
    claims = json.loads(base64.urlsafe_b64decode(payload + "=" * (-len(payload) % 4)))
    depois = datetime.fromtimestamp(claims["exp"] + 3600, timezone.utc)
    with time_machine.travel(depois, tick=False):
        assert cliente.get("/auth/me", headers=headers).status_code == 401


def test_usuario_comum_sem_permissao_administrativa(cliente, autenticar, evento):
    headers = autenticar()
    assert cliente.post("/eventos", json=evento, headers=headers).status_code == 403


def test_administrador_cadastra_evento(cliente, autenticar, evento):
    resposta = cliente.post("/eventos", json=evento, headers=autenticar(admin=True))
    assert resposta.status_code == 201
    assert resposta.json()["titulo"] == evento["titulo"]


@pytest.mark.parametrize("alteracao", [
    {"nome": "  "}, {"email": "invalido"}, {"senha": "curta"},
    {"senha": "        "}, {"perfil": "administrador"},
])
def test_cadastro_invalido_preserva_sigilo(cliente, usuario, alteracao):
    entrada = usuario | alteracao
    resposta = cliente.post("/usuarios", json=entrada)
    assert resposta.status_code == 422
    assert entrada["senha"] not in resposta.text


def test_assinatura_invalida(cliente, autenticar):
    token, assinatura = autenticar()["Authorization"].rsplit(".", 1)
    alterada = ("A" if assinatura[0] != "A" else "B") + assinatura[1:]
    assert cliente.get("/auth/me", headers={"Authorization": f"{token}.{alterada}"}).status_code == 401


def test_inscricao_com_perfil_usuario(cliente, autenticar, participante, evento):
    admin = autenticar(admin=True)
    eid = cliente.post("/eventos", json=evento, headers=admin).json()["id"]
    pid = cliente.post("/participantes", json=participante, headers=admin).json()["id"]
    conta = dict(nome="Ana", email=participante["email"], senha="OutraSenha123")
    assert cliente.post("/usuarios", json=conta).status_code == 201
    token = cliente.post("/auth/login", json={k: conta[k] for k in ("email", "senha")}).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    assert cliente.get(f"/participantes/{pid}", headers=headers).status_code == 200
    assert cliente.post(f"/eventos/{eid}/inscricoes/{pid}", headers=headers).status_code == 201
    assert cliente.delete(f"/eventos/{eid}", headers=headers).status_code == 403
    assert cliente.get("/relatorios/eventos/ocupacao", headers=headers).status_code == 403
