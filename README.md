# APS 2 — Eventos acadêmicos

Projeto da APS 2 da matéria de Desenvolvimento Backend: uma API para um site de eventos acadêmicos.

## Organização do código

O projeto utiliza arquitetura em camadas. Cada parte fica em um módulo próprio dentro de `app/`:

```text
.
├── app/
│   ├── main.py
│   ├── models/
│   ├── repositories/
│   ├── services/
│   └── routers/
└── README.md
```

- **`app/models`**: define os formatos dos dados e as regras de validação, por exemplo os campos obrigatórios de um evento. Com Pydantic, esses modelos também validam os dados recebidos pela API.
- **`app/repositories`**: lê e grava dados. É a camada que conversa com a fonte de dados (por exemplo, banco de dados); não deve decidir regras do negócio nem conhecer detalhes HTTP.
- **`app/services`**: implementa as regras do negócio e coordena as operações necessárias. Por exemplo, verifica se um evento pode ser criado e chama o repositório para salvá-lo.
- **`app/routers`**: declara os endpoints e métodos HTTP (`GET`, `POST`, `PUT`/`PATCH`, `DELETE`), recebe parâmetros e corpos das requisições, chama os serviços e define as respostas HTTP.
- **`app/main.py`**: cria a aplicação FastAPI e registra os routers. Deve ser o ponto de entrada, sem concentrar ali a lógica das funcionalidades.

O fluxo normal de uma requisição é:

```text
cliente → router → service → repository → fonte de dados
                         ← resultado ←
```

Exemplo para a funcionalidade de eventos: o router recebe `POST /eventos`, o service aplica as regras de criação, o repository persiste o evento e o router devolve a resposta HTTP. A validação do formato dos dados fica no model.

> No início, `app/main.py` está na raiz e vazio. Ao adotar essa estrutura, mova o ponto de entrada para `app/main.py` e inicie a aplicação por esse módulo. Os nomes e a divisão podem ser ajustados conforme os requisitos da APS.
