# APS 4 — Eventos acadêmicos

API FastAPI para eventos, participantes, inscrições e relatórios, com autenticação por JWT e persistência em SQLite usando SQLAlchemy.

As rotas ficam em `app/routers`, as regras de negócio em `services`, o acesso aos dados em `repositories`, as entidades em `models` e a validação em `schemas`. O arquivo `app/security.py` cuida das senhas e dos tokens.

## Executar

Na pasta `aps2`, use Python 3.14 e execute os comandos do seu sistema.

### Windows

```powershell
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
$env:JWT_SECRET = .\venv\Scripts\python.exe -c "import secrets; print(secrets.token_urlsafe(48))"
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

### Linux

```sh
python3 -m venv venv
venv/bin/python -m pip install -r requirements.txt
export JWT_SECRET="$(venv/bin/python -c 'import secrets; print(secrets.token_urlsafe(48))')"
venv/bin/python -m uvicorn app.main:app --reload
```

Os comandos geram uma chave para a sessão do terminal. Para manter os tokens válidos entre reinícios, configure o mesmo `JWT_SECRET` no ambiente do servidor.

## Swagger

Acesse http://127.0.0.1:8000/docs para testar as rotas.

1. Em `POST /usuarios`, envie nome, e-mail e senha. Exemplo: `{"nome":"Ana","email":"ana@example.com","senha":"Exemplo123"}`.
2. Em `POST /auth/login`, envie o mesmo e-mail e senha. Copie o `access_token` e cole em **Authorize**. O token vale por 30 minutos.
3. Execute `GET /auth/me` para conferir a conta e o perfil.

O cadastro público cria usuários comuns. Para criar um administrador, execute `.\venv\Scripts\python.exe -m app.criar_admin` no Windows ou `venv/bin/python -m app.criar_admin` no Linux.

| Rotas | Métodos | Acesso |
|---|---|---|
| `/usuarios`, `/auth/login` | POST | Público |
| `/auth/me` | GET | Autenticado |
| `/eventos`, `/eventos/{id}` | GET | Público |
| `/participantes`, `/participantes/{id}` | GET | Autenticado |
| `/eventos`, `/participantes` | POST | Administrador |
| `/eventos/{id}`, `/participantes/{id}` | PUT, DELETE | Administrador |
| `/eventos/{evento_id}/inscricoes/{participante_id}` | POST | Autenticado |
| `/eventos/{evento_id}/inscricoes` | GET | Autenticado |
| `/relatorios/eventos/ocupacao`, `/relatorios/eventos/categorias`, `/relatorios/participantes/cursos` | GET | Administrador |

## Banco de dados

A configuração fica em `database/db.py`. Ao iniciar, a API cria as tabelas em `database.db` e preserva os registros existentes. As senhas são armazenadas como hashes Argon2id.

## Testes

Na raiz do projeto, execute a suíte de regras de negócio, rotas e autenticação com cobertura:

```powershell
.\venv\Scripts\python.exe -m pytest tests --cov=app --cov=database --cov-fail-under=80
```

No Linux, use `venv/bin/python` no lugar de `.\venv\Scripts\python.exe`.
