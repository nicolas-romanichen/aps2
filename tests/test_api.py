import pytest


@pytest.fixture
def api(cliente, autenticar):
    cliente.headers.update(autenticar(admin=True))
    return cliente


@pytest.mark.parametrize("rota,fixture,campo,novo", [
    ("/eventos", "evento", "local", "Auditório"),
    ("/participantes", "participante", "curso", "Direito"),
])
def test_ciclo_de_cadastro(api, request, rota, fixture, campo, novo):
    dados = request.getfixturevalue(fixture)
    resposta = api.post(rota, json=dados)
    assert resposta.status_code == 201
    registro = resposta.json()
    recurso = f"{rota}/{registro['id']}"
    assert registro == dados | {"id": registro["id"]}
    assert api.get(rota).json() == [registro]
    alteracao = api.put(recurso, json=dados | {campo: novo})
    assert alteracao.status_code == 200
    assert api.get(recurso).json() == registro | {campo: novo}
    assert api.delete(recurso).status_code == 200
    assert api.get(recurso).status_code == 404


@pytest.mark.parametrize("rota,fixture,alteracoes", [
    ("/eventos", "evento", {"capacidade": 0}),
    ("/participantes", "participante", {"email": "invalido"}),
])
def test_cadastro_invalido(api, request, rota, fixture, alteracoes):
    resposta = api.post(rota, json=request.getfixturevalue(fixture) | alteracoes)
    assert resposta.status_code == 422
    assert api.get(rota).json() == []


def test_inscricao_e_relatorios(api, evento, participante):
    eid = api.post("/eventos", json=evento).json()["id"]
    pessoa = api.post("/participantes", json=participante).json()
    rota = f"/eventos/{eid}/inscricoes"
    inscricao = f"{rota}/{pessoa['id']}"
    assert api.post(inscricao).status_code == 201
    assert api.post(inscricao).status_code == 409
    assert api.get(rota).json() == [pessoa]
    assert api.get("/relatorios/eventos/ocupacao").json() == [
        dict(evento_id=eid, titulo="Oficina", capacidade=2, total_inscritos=1,
             vagas_disponiveis=1, percentual_ocupacao=50)]
    assert api.get("/relatorios/eventos/categorias").json() == [
        dict(categoria="Extensão", total_eventos=1, capacidade_total=2, total_inscricoes=1)]
    assert api.get("/relatorios/participantes/cursos").json() == [
        dict(curso="Computação", total_participantes=1, total_inscricoes=1)]
    assert api.delete(f"/participantes/{pessoa['id']}").status_code == 200
    assert api.get(rota).json() == []
