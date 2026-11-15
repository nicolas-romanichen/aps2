# APS 3 — Eventos acadêmicos

API FastAPI para eventos, participantes e inscrições, com relatórios e persistência em SQLite usando SQLAlchemy.

Camadas: `routers` (HTTP), `services` (regras), `repositories` (dados), `models` (entidades) e `schemas` (validação).

## Executar

Execute os comandos dentro da pasta `aps2`.

### Windows

```powershell
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe -B -m uvicorn app.main:app --reload
```

### Linux

```sh
python3 -m venv venv
venv/bin/python -m pip install -r requirements.txt
venv/bin/python -B -m uvicorn app.main:app --reload
```

## Swagger

Acesse http://127.0.0.1:8000/docs para testar as rotas.

| Rotas | Métodos |
|---|---|
| `/eventos`, `/participantes` | POST (cadastrar), GET (listar) |
| `/eventos/{id}`, `/participantes/{id}` | GET (consultar), PUT (atualizar), DELETE (excluir) |
| `/eventos/{evento_id}/inscricoes/{participante_id}` | POST (inscrever) |
| `/eventos/{evento_id}/inscricoes` | GET (listar inscritos) |
| `/relatorios/eventos/ocupacao` | GET (ocupação e vagas) |
| `/relatorios/eventos/categorias` | GET (totais por categoria) |
| `/relatorios/participantes/cursos` | GET (participação por curso) |

## Banco de dados

A configuração fica em `database/db.py`. O arquivo `aps2/database.db` e as tabelas de eventos, participantes e inscrições são criados automaticamente ao iniciar a API.

Os dados permanecem salvos após reiniciar. Os relatórios consultam esses registros. Ao excluir um evento ou participante, suas inscrições também são removidas.
