# APS 2 — Eventos acadêmicos

API FastAPI para eventos, participantes e inscrições. Camadas: `routers` (HTTP), `services` (regras), `repositories` (dados) e `models` (Pydantic).

### LINUX
```sh
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### WINDOWS
```sh
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Utilize o Swagger
Abra http://127.0.0.1:8000/docs para testar pelo Swagger. Os dados ficam em memória e são perdidos ao reiniciar; execute com um único processo.


| Rotas | Métodos |
|---|---|
| `/eventos`, `/participantes` | POST (cadastrar), GET (listar) |
| `/eventos/{id}`, `/participantes/{id}` | GET (consultar), PUT (substituir), DELETE (excluir) |
| `/eventos/{evento_id}/inscricoes/{participante_id}` | POST (inscrever) |
| `/eventos/{evento_id}/inscricoes` | GET (listar participantes inscritos) |
