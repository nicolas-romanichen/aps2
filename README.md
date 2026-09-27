# APS 2 — Eventos acadêmicos

API FastAPI para eventos, participantes e inscrições. Camadas: `routers` (HTTP), `services` (regras), `repositories` (dados) e `models` (Pydantic).


```sh
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Abra http://127.0.0.1:8000/docs para testar pelo Swagger. Os dados ficam em memória e são perdidos ao reiniciar; execute com um único processo.

| Rotas | Métodos |
|---|---|
| `/eventos`, `/participantes` | POST (cadastrar), GET (listar) |
| `/eventos/{id}`, `/participantes/{id}` | GET (consultar), PUT (substituir), DELETE (excluir) |
| `/eventos/{evento_id}/inscricoes/{participante_id}` | POST (inscrever) |
| `/eventos/{evento_id}/inscricoes` | GET (listar participantes inscritos) |

Exemplo de corpo para `POST /eventos`:

```json
{"titulo":"Python","descricao":"Minicurso introdutório","data":"2026-11-20","horario":"14:00:00","local":"Lab 1","capacidade":20,"categoria":"Minicurso"}
```

Resposta `201`: o mesmo objeto com `"id": 1`. Para `POST /participantes`:

```json
{"nome":"Ana","email":"ana@example.com","curso":"Computação"}
```

Com os IDs retornados, `POST /eventos/1/inscricoes/1` (sem corpo) responde `201`:

```json
{"evento_id":1,"participante_id":1}
```

Consultas e atualizações retornam `200`; exclusões, `204` sem corpo. Erros: `404` para recurso inexistente, `400` para inscrição repetida/falta de vagas/capacidade abaixo dos inscritos e `422` para dados inválidos. Exemplo de erro:

```json
{"detail":"Evento não encontrado."}
```
