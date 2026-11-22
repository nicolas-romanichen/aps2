# APS 4 — Segurança na API de eventos acadêmicos

A API FastAPI gerencia eventos, participantes, inscrições e relatórios da APS 3. A APS 4 acrescenta contas de acesso, autenticação por e-mail e senha, tokens JWT e autorização por perfil. O usuário é a conta de acesso. O participante é o registro acadêmico utilizado nas inscrições.

## Instalação e execução

Na raiz do repositório, use Python 3.14 e crie um ambiente virtual. No PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\python -m pip install -r requirements.txt
$env:JWT_SECRET = .\venv\Scripts\python -c "import secrets; print(secrets.token_urlsafe(48))"
.\venv\Scripts\python -m uvicorn app.main:app --reload
```

No Linux ou macOS:

```sh
python3 -m venv venv
venv/bin/python -m pip install -r requirements.txt
export JWT_SECRET="$(venv/bin/python -c 'import secrets; print(secrets.token_urlsafe(48))')"
venv/bin/python -m uvicorn app.main:app --reload
```

A chave gerada vale para a sessão do terminal. Para manter os tokens válidos após reiniciar a aplicação, configure o mesmo valor no ambiente do servidor. A aplicação exige pelo menos 32 bytes de chave. O PyJWT assina os tokens com HS256 e verifica assinatura e expiração. O token identifica o usuário por `sub`, expira em 30 minutos e o servidor consulta o perfil atual no SQLite a cada requisição protegida.

A inicialização cria as tabelas ausentes em `database.db` na raiz do projeto. Um banco da APS 3 mantém seus registros e recebe a tabela `usuarios`.

## Cadastro e administrador inicial

O cadastro público cria contas com perfil `usuario`. O nome e o e-mail são obrigatórios. O e-mail é normalizado para minúsculas e deve ser único. A senha deve ter entre 8 e 128 caracteres e conter pelo menos um caractere diferente de espaço. A biblioteca argon2-cffi gera e verifica hashes Argon2id com salt individual.

Para criar uma conta administrativa, abra outro terminal na raiz e execute `.\venv\Scripts\python -m app.criar_admin` no Windows ou `venv/bin/python -m app.criar_admin` no Linux. Informe nome, e-mail livre e senha no prompt local. O comando escreve no mesmo SQLite da API. O acesso ao arquivo de banco e a esse terminal deve ficar restrito ao responsável pela instalação.

## Permissões das rotas

| Acesso | Métodos e caminhos |
|---|---|
| Público | `POST /usuarios`, `POST /auth/login`, `GET /eventos`, `GET /eventos/{id}` |
| Documentação pública | `GET /docs`, `GET /redoc`, `GET /openapi.json` |
| Usuário ou administrador | `GET /auth/me`, `GET /participantes`, `GET /participantes/{id}` |
| Usuário ou administrador | `POST /eventos/{evento_id}/inscricoes/{participante_id}`, `GET /eventos/{evento_id}/inscricoes` |
| Administrador | `POST /eventos`, `PUT /eventos/{id}`, `DELETE /eventos/{id}` |
| Administrador | `POST /participantes`, `PUT /participantes/{id}`, `DELETE /participantes/{id}` |
| Administrador | `GET /relatorios/eventos/ocupacao`, `GET /relatorios/eventos/categorias`, `GET /relatorios/participantes/cursos` |

A equipe adotou consulta pública de eventos, consulta autenticada de participantes e inscritos e administração dos cadastros e relatórios pelo perfil administrativo. Qualquer conta autenticada pode inscrever um participante cadastrado, respeitando a capacidade e a unicidade da inscrição.

## Demonstração pelo Swagger

Abra `http://127.0.0.1:8000/docs`. Em cada operação, clique em **Try it out** e **Execute**. Em **Authorize**, cole apenas o valor de `access_token`. O Swagger monta o cabeçalho `Authorization: Bearer <token>`. Use **Logout** para trocar de perfil. Para repetir a demonstração, use um e-mail novo e os IDs retornados pela sua execução.

| Cenário | Requisição ou verificação | Resultado esperado |
|---|---|---|
| 1. Cadastro | `POST /usuarios` com `{"nome":"Ana","email":"ana@example.com","senha":"Exemplo-de-aula123"}` | 201, com id, nome, e-mail e perfil `usuario` |
| 2. Armazenamento | Consulte o SQLite com o comando abaixo após o cadastro | Prefixo `$argon2id$`. O teste também verifica o hash pela biblioteca |
| 3. Duplicidade | Repita o primeiro cadastro | 409 |
| 4. Login | `POST /auth/login` com o e-mail e a senha do cadastro, sem o campo nome | 200, com `access_token` e `token_type: bearer` |
| 5. Credenciais incorretas | Repita o login com senha errada, depois com e-mail inexistente | 401 e a mesma mensagem nos dois casos |
| 6. Sem token | Execute `GET /auth/me` antes de autorizar | 401 |
| 7. Token válido | Autorize o token de Ana e execute `GET /participantes` | 200 e uma lista |
| 8. Token inválido ou expirado | Em **Authorize**, use `invalido`, ou reutilize o token depois de 30 minutos, e execute `GET /auth/me` | 401. A suíte automatiza a expiração avançando o relógio do teste |
| 9. Ação administrativa com perfil comum | Com o token de Ana, envie o evento abaixo a `POST /eventos` | 403 |
| 10. Ação administrativa autorizada | Faça login com a conta do comando local, autorize o novo token e repita a criação do evento | 201, com o ID do evento |
| 11. Identidade | Execute `GET /auth/me` com cada token válido | 200 e dados da conta correspondente, sem senha ou hash |
| 12. Continuidade | Como administrador, crie o participante abaixo. Como Ana, faça a inscrição com os IDs retornados. Como administrador, consulte os três relatórios | 201 nos cadastros e na inscrição, 200 nos relatórios. Com apenas estes dados, o evento tem 50% de ocupação e uma vaga livre |

Evento de exemplo para os cenários 9 e 10:

```json
{"titulo":"Oficina","descricao":"Introdução","data":"2027-04-12","horario":"09:00:00","local":"Sala 1","capacidade":2,"categoria":"Extensão"}
```

Participante para o cenário 12:

```json
{"nome":"Ana","email":"ana@example.com","curso":"Computação"}
```

No PowerShell, confira o algoritmo gravado sem exibir o hash completo:

```powershell
.\venv\Scripts\python -c "import sqlite3; print(sqlite3.connect('database.db').execute('SELECT email, substr(senha_hash, 1, 10) FROM usuarios').fetchall())"
```

Uma inscrição duplicada ou sem vagas retorna 409. Recursos inexistentes retornam 404 e entradas com campos inválidos retornam 422.

### Resultados obtidos

Na demonstração pelo Swagger UI em banco vazio, o cadastro retornou 201 e a repetição retornou 409. A verificação direta do banco confirmou o hash Argon2id. O login com senha incorreta retornou 401 e o login válido retornou 200. A consulta a `/auth/me` retornou 401 sem token, 401 com token inválido e 200 com o token da conta cadastrada.

A criação do mesmo evento retornou 403 com o perfil comum e 201 com o administrador criado pelo comando local. O administrador cadastrou o participante (201) e a conta comum realizou a inscrição (201). Os três relatórios retornaram 200, com 50% de ocupação e uma inscrição nos totais de categoria e curso. O teste automatizado de expiração confirmou 401 após o vencimento.

## Organização e testes

| Caminho | Responsabilidade |
|---|---|
| `app/main.py`, `app/dependencies.py` | Inicialização, tratamento de erros, injeção de serviços e permissões |
| `app/routers/`, `app/schemas/` | Rotas HTTP e contratos de entrada e saída |
| `app/services/`, `app/security.py` | Regras de negócio, autenticação, hashing e JWT |
| `app/models/`, `app/repositories/`, `database/db.py` | Modelos SQLAlchemy, consultas, sessões e transações SQLite |
| `tests/` | Regras de negócio isoladas e testes HTTP com SQLite temporário |

No Windows, execute na raiz:

```powershell
.\venv\Scripts\python -m pip install -r requirements-test.txt
.\venv\Scripts\python -m pytest tests -v --cov=app --cov=database --cov-report=term-missing --cov-fail-under=80
```

No Linux, substitua o executável por `venv/bin/python`. Os testes configuram uma chave efêmera e um banco próprio para cada caso HTTP. Para ver os métodos, caminhos e códigos HTTP durante a suíte, acrescente `--log-cli-level=INFO`.

[Repositório da APS 4 no GitHub](https://github.com/nicolas-romanichen/aps2/tree/aps4)
