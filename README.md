# APS 3 — Eventos acadêmicos

Evolução da APS 2 com FastAPI, Pydantic, SQLite e SQLAlchemy ORM. Eventos, participantes e inscrições são persistidos; os três relatórios são calculados a partir dos dados atuais do banco.

## Instalação e execução

Use Python 3.10 ou superior (validado com Python 3.14). Execute os comandos dentro de `aps2`.

Windows / PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe -B -m uvicorn app.main:app --reload
```

Linux/macOS:

```sh
python3 -m venv venv
venv/bin/python -m pip install -r requirements.txt
venv/bin/python -B -m uvicorn app.main:app --reload
```

Acesse o Swagger em http://127.0.0.1:8000/docs. Em cada rota, use **Try it out**, preencha os parâmetros/JSON e clique em **Execute**. O esquema OpenAPI está em `/openapi.json`.

## Estrutura e responsabilidades

- `app/main.py`: aplicação, inicialização e tratamento de erros.
- `database/db.py`: conexão, sessões, transações e criação de tabelas.
- `app/models`: entidades SQLAlchemy e relacionamentos.
- `app/schemas`: validações e respostas Pydantic.
- `app/routers`: controllers HTTP; a representação de saída é JSON.
- `app/services`: regras de negócio e coordenação das operações.
- `app/repositories`: persistência e consultas agregadas.

## Banco e integridade

O banco é **`aps2/database.db`**, calculado em relação ao arquivo de configuração e independente da pasta de execução. Ele e suas tabelas são criados automaticamente na inicialização. Não é necessário criar tabelas manualmente nem instalar um servidor de banco. Arquivos `db.db` ou outros `database.db` não são usados pela aplicação.

As tabelas são `eventos`, `participantes` e `inscricoes`. IDs são gerados pelo SQLite; inscrições têm ID, duas chaves estrangeiras e `data_inscricao`, preenchida pelo servidor na data de São Paulo (`YYYY-MM-DD`). Cada evento e participante tem uma coleção de inscrições; cada inscrição referencia um evento e um participante.

Cada requisição recebe uma sessão. Alterações são confirmadas antes de enviar a resposta; falhas provocam rollback e a sessão sempre é fechada. Uma transação `BEGIN IMMEDIATE` reserva a escrita antes de verificar as vagas, protegendo a última vaga contra concorrência. As operações de dados e relatórios usam SQLAlchemy; o comando de transação e o PRAGMA de chaves estrangeiras são apenas configuração do SQLite.

E-mails são normalizados para minúsculas e têm restrição única no banco. O par evento/participante também é único. Chaves estrangeiras são ativadas em cada conexão e capacidade tem restrição positiva.

Excluir um evento ou participante remove suas inscrições na mesma transação, sem excluir a outra entidade. Não é permitido reduzir a capacidade abaixo da quantidade de inscritos. PUT substitui os campos editáveis e exige todos eles. Categorias e cursos são textos livres, agrupados pelo valor armazenado.

O banco local não é versionado. Para transferir dados, copie `database.db` com a aplicação parada. A criação automática não migra estruturas antigas: esta versão parte de um banco vazio; alterações futuras de esquema exigirão migração. A reinicialização normal nunca apaga os registros.

## Rotas e respostas

| Métodos | Rota | Função |
|---|---|---|
| POST / GET | `/eventos` | Cadastrar / listar |
| GET / PUT / DELETE | `/eventos/{id}` | Consultar / atualizar / excluir |
| POST / GET | `/participantes` | Cadastrar / listar |
| GET / PUT / DELETE | `/participantes/{id}` | Consultar / atualizar / excluir |
| POST | `/eventos/{evento_id}/inscricoes/{participante_id}` | Inscrever |
| GET | `/eventos/{evento_id}/inscricoes` | Listar participantes inscritos |
| GET | `/relatorios/eventos/ocupacao` | Ocupação por evento |
| GET | `/relatorios/eventos/categorias` | Totais por categoria |
| GET | `/relatorios/participantes/cursos` | Participação por curso |

Cadastros retornam 201; consultas, atualizações e exclusões, 200. Ausência de recurso retorna 404; duplicidade, falta de vagas e redução indevida de capacidade, 409; entrada inválida, 422; falha inesperada de persistência, 500. Erros usam `detail`, sem expor SQL ou detalhes internos. Exclusões mantêm a resposta `codigo` e `mensagem` da APS 2.

## Exemplos JSON

POST `/eventos`:

```json
{"titulo":"Python","descricao":"Introdução","data":"2026-12-10","horario":"19:00:00","local":"Sala 1","capacidade":2,"categoria":"Palestra"}
```

A resposta 201 contém os mesmos campos mais `id`. POST `/participantes`:

```json
{"nome":"Ana","email":"ana@example.com","curso":"Software"}
```

A resposta 201 inclui `id`. Use os IDs retornados em POST `/eventos/1/inscricoes/1`. Exemplo de resposta (data ilustrativa):

```json
{"id":1,"evento_id":1,"participante_id":1,"data_inscricao":"2026-11-15"}
```

Uma segunda inscrição do mesmo participante retorna 409:

```json
{"detail":"Participante já está inscrito neste evento."}
```

## Relatórios

- **Ocupação:** `evento_id`, `titulo`, `capacidade`, `total_inscritos`, `vagas_disponiveis`, `percentual_ocupacao`. Vagas = capacidade − inscritos; percentual = inscritos × 100 / capacidade, arredondado para duas casas. Inclui eventos vazios e protege a divisão por zero. Ordenação por ID.
- **Categorias:** `categoria`, `total_eventos`, `capacidade_total`, `total_inscricoes`. Inscrições são agregadas antes da soma das capacidades, evitando multiplicação de valores. Ordenação por categoria.
- **Cursos:** `curso`, `total_participantes`, `total_inscricoes`. Participantes distintos são contados uma vez mesmo com várias inscrições. Inclui cursos sem inscrições. Ordenação por curso.

Todos retornam listas JSON e `[]` com status 200 quando não existem registros. Não há listas fixas nem totais armazenados: alterações no banco aparecem na próxima consulta.

## Roteiro obrigatório no Swagger

Use uma base de demonstração separada de dados importantes. Anote os IDs reais devolvidos pela API; os passos não dependem de IDs começarem em 1.

1. Cadastre dois eventos da categoria Palestra com capacidade 2 e um Workshop sem inscrições. Consulte a lista e cada evento.
2. Cadastre Ana e Bruno no curso Software e Clara no curso Direito. Consulte participantes e cada registro.
3. Inscreva Ana nos dois primeiros eventos e Bruno apenas no primeiro. Consulte os inscritos. Confira `id` e `data_inscricao` nas respostas de criação.
4. Repita a inscrição de Ana no primeiro evento: 409. Tente inscrever Clara no primeiro evento lotado: 409.
5. Use um evento inexistente e depois um participante inexistente: 404. Tente repetir um e-mail: 409.
6. Consulte os três relatórios e compare com os valores da tabela abaixo.
7. Encerre o Uvicorn com Ctrl+C e execute novamente. Consulte eventos, participantes, inscrições e relatórios; os dados devem permanecer.
8. Atualize o segundo evento para capacidade 4 e categoria Workshop. A ocupação dele deve passar a 25%; Workshop deve ter 2 eventos, capacidade 6 e 1 inscrição.
9. Atualize Ana para o curso Direito. Direito passa a ter 2 participantes e 2 inscrições; Software, 1 participante e 1 inscrição.
10. Tente reduzir a capacidade do primeiro evento para 1: 409. Teste nome/título vazios, e-mail inválido, data/horário inválidos, campos ausentes e capacidade zero: 422.
11. Exclua Ana: suas duas inscrições desaparecem e os demais participantes/eventos permanecem. O primeiro evento passa a ter 1 inscrito e o segundo, zero.
12. Exclua o primeiro evento: sua inscrição restante desaparece. Consulte os relatórios novamente. Confira também consultas/exclusões de IDs inexistentes (404).

Valores esperados antes das alterações:

| Relatório | Resultado |
|---|---|
| Primeiro evento | 2 inscritos, 0 vagas, 100% |
| Segundo evento | 1 inscrito, 1 vaga, 50% |
| Evento vazio | 0 inscritos, 2 vagas, 0% |
| Palestra | 2 eventos, capacidade 4, 3 inscrições |
| Workshop | 1 evento, capacidade 2, 0 inscrições |
| Software | 2 participantes, 3 inscrições |
| Direito | 1 participante, 0 inscrições |

Registre capturas do Swagger mostrando entrada, status e resposta, inclusive antes/depois do reinício e das alterações.

## Entrega

Entregar o código completo, `requirements.txt`, este README e o link do repositório atualizado no GitHub. Incluir as evidências da demonstração pelo Swagger. Repositório configurado: https://github.com/nicolas-romanichen/aps2. A publicação no GitHub deve ser feita após revisar as alterações locais.
