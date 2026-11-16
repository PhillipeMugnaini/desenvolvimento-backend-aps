# API de Eventos Acadêmicos

## Descrição

Este projeto consiste no desenvolvimento de uma API RESTful para gerenciamento de eventos acadêmicos.

A aplicação permite cadastrar, consultar, atualizar e excluir eventos e participantes, além de realizar inscrições de participantes em eventos.

O projeto foi desenvolvido utilizando Python, FastAPI e Pydantic, aplicando conceitos de APIs RESTful, métodos HTTP, códigos de status, validação de dados, tratamento de erros e separação de responsabilidades utilizando arquitetura MVC.

Os dados são armazenados em memória através de listas Python, não sendo necessário banco de dados nesta versão da aplicação.

---

## Tecnologias utilizadas

- Python
- FastAPI
- Pydantic
- Uvicorn
- Swagger UI

---

## Estrutura do projeto

```text
04 APS2/
│
├── main.py
├── requirements.txt
├── README.md
│
├── controller/
│   ├── evento_controller.py
│   ├── participante_controller.py
│   └── inscricao_controller.py
│
├── model/
│   ├── evento.py
│   └── participante.py
│
└── service/
    ├── evento_service.py
    ├── participante_service.py
    └── inscricao_service.py
```

### Model

Responsável pela representação e validação dos dados utilizando Pydantic.

### Controller

Responsável pelas rotas da API, recebimento das requisições HTTP e retorno das respostas.

### Service

Responsável pelas regras de negócio da aplicação, como criação, busca, atualização, exclusão e validação das inscrições.

---

# Instalação

## 1. Clonar o repositório

```bash
git clone URL_DO_REPOSITORIO
```

Depois entre na pasta do projeto:

```bash
cd "04 APS2"
```

---

## 2. Criar o ambiente virtual

No Linux:

```bash
python3 -m venv venv
```

---

## 3. Ativar o ambiente virtual

No Linux:

```bash
source venv/bin/activate
```

Quando ativado, o terminal deverá apresentar algo parecido com:

```text
(venv) usuario@computador:~/projeto$
```

---

## 4. Instalar as dependências

```bash
pip install -r requirements.txt
```

---

# Executando a aplicação

Com o ambiente virtual ativado, execute:

```bash
uvicorn main:app --reload
```

A API estará disponível em:

```text
http://127.0.0.1:8000
```

---

# Swagger

O FastAPI disponibiliza automaticamente uma interface para documentação e testes da API.

Acesse:

```text
http://127.0.0.1:8000/docs
```

Nesta página é possível testar todas as rotas da aplicação.

---

# Rotas de Eventos

## Cadastrar evento

```http
POST /eventos
```

Exemplo de requisição:

```json
{
  "titulo": "Workshop de FastAPI",
  "descricao": "Workshop prático sobre desenvolvimento de APIs RESTful",
  "data": "2026-10-20",
  "horario": "19:00:00",
  "local": "Sala 10",
  "capacidade": 50,
  "categoria": "Workshop"
}
```

Exemplo de resposta:

```json
{
  "titulo": "Workshop de FastAPI",
  "descricao": "Workshop prático sobre desenvolvimento de APIs RESTful",
  "data": "2026-10-20",
  "horario": "19:00:00",
  "local": "Sala 10",
  "capacidade": 50,
  "categoria": "Workshop",
  "id": 1
}
```

Status esperado:

```text
201 Created
```

---

## Listar eventos

```http
GET /eventos
```

Retorna todos os eventos cadastrados.

Exemplo:

```json
[
  {
    "titulo": "Workshop de FastAPI",
    "descricao": "Workshop prático sobre desenvolvimento de APIs RESTful",
    "data": "2026-10-20",
    "horario": "19:00:00",
    "local": "Sala 10",
    "capacidade": 50,
    "categoria": "Workshop",
    "id": 1
  }
]
```

---

## Consultar evento por ID

```http
GET /eventos/{evento_id}
```

Exemplo:

```http
GET /eventos/1
```

Caso o evento não exista:

```json
{
  "detail": "Evento não encontrado."
}
```

Status:

```text
404 Not Found
```

---

## Atualizar evento

```http
PUT /eventos/{evento_id}
```

Exemplo:

```http
PUT /eventos/1
```

Corpo da requisição:

```json
{
  "titulo": "Workshop Avançado de FastAPI",
  "descricao": "Workshop atualizado",
  "data": "2026-10-21",
  "horario": "20:00:00",
  "local": "Auditório Principal",
  "capacidade": 100,
  "categoria": "Workshop"
}
```

---

## Excluir evento

```http
DELETE /eventos/{evento_id}
```

Exemplo:

```http
DELETE /eventos/1
```

Em caso de sucesso:

```text
204 No Content
```

Caso o evento não exista:

```json
{
  "detail": "Evento não encontrado."
}
```

---

# Rotas de Participantes

## Cadastrar participante

```http
POST /participantes
```

Exemplo:

```json
{
  "nome": "Phillipe Mugnaini",
  "email": "phillipe@email.com",
  "curso": "Engenharia de Software"
}
```

Exemplo de resposta:

```json
{
  "nome": "Phillipe Mugnaini",
  "email": "phillipe@email.com",
  "curso": "Engenharia de Software",
  "id": 1
}
```

Status esperado:

```text
201 Created
```

---

## Listar participantes

```http
GET /participantes
```

Exemplo de resposta:

```json
[
  {
    "nome": "Phillipe Mugnaini",
    "email": "phillipe@email.com",
    "curso": "Engenharia de Software",
    "id": 1
  }
]
```

---

## Consultar participante

```http
GET /participantes/{participante_id}
```

Exemplo:

```http
GET /participantes/1
```

Caso não seja encontrado:

```json
{
  "detail": "Participante não encontrado."
}
```

---

## Atualizar participante

```http
PUT /participantes/{participante_id}
```

Exemplo:

```json
{
  "nome": "Phillipe Mugnaini",
  "email": "phillipe.novo@email.com",
  "curso": "Engenharia de Software"
}
```

---

## Excluir participante

```http
DELETE /participantes/{participante_id}
```

Em caso de sucesso:

```text
204 No Content
```

---

# Inscrições

## Inscrever participante em um evento

```http
POST /eventos/{evento_id}/inscricoes/{participante_id}
```

Exemplo:

```http
POST /eventos/1/inscricoes/1
```

Resposta:

```json
{
  "evento_id": 1,
  "participante_id": 1
}
```

Status:

```text
201 Created
```

Antes de realizar uma inscrição, a aplicação verifica:

- se o evento existe;
- se o participante existe;
- se o participante já está inscrito no evento;
- se o evento ainda possui vagas disponíveis.

---

## Participante já inscrito

Caso o mesmo participante tente se inscrever novamente:

```json
{
  "detail": "Participante já está inscrito neste evento."
}
```

Status:

```text
400 Bad Request
```

---

## Evento sem vagas

Caso a capacidade máxima tenha sido atingida:

```json
{
  "detail": "Não existem vagas disponíveis para este evento."
}
```

Status:

```text
400 Bad Request
```

---

## Listar participantes inscritos em um evento

```http
GET /eventos/{evento_id}/inscricoes
```

Exemplo:

```http
GET /eventos/1/inscricoes
```

Exemplo de resposta:

```json
[
  {
    "nome": "Phillipe Mugnaini",
    "email": "phillipe@email.com",
    "curso": "Engenharia de Software",
    "id": 1
  },
  {
    "nome": "Lucas Ferreira",
    "email": "lucas@email.com",
    "curso": "Engenharia de Software",
    "id": 2
  }
]
```

---

# Validação de dados

A aplicação utiliza o Pydantic para validar automaticamente os dados enviados para a API.

Entre as validações implementadas estão:

- título do evento obrigatório;
- título do evento não pode ser vazio;
- capacidade deve ser maior que zero;
- data deve possuir formato válido;
- horário deve possuir formato válido;
- nome do participante obrigatório;
- nome do participante não pode ser vazio;
- e-mail deve possuir formato válido;
- campos obrigatórios devem ser informados.

Quando os dados enviados não atendem ao formato esperado, o FastAPI retorna:

```text
422 Unprocessable Entity
```

Exemplo de requisição inválida:

```json
{
  "nome": "",
  "email": "email-invalido",
  "curso": "Engenharia de Software"
}
```

---

# Códigos HTTP utilizados

| Código | Significado | Utilização |
|---|---|---|
| 200 | OK | Consultas e atualizações realizadas |
| 201 | Created | Cadastro e inscrição realizados |
| 204 | No Content | Exclusão realizada |
| 400 | Bad Request | Regra de negócio inválida |
| 404 | Not Found | Recurso não encontrado |
| 422 | Unprocessable Entity | Dados inválidos enviados para a API |

---

# Armazenamento

Nesta versão do projeto não é utilizado banco de dados.

Os dados são armazenados em listas Python durante a execução da aplicação:

```python
eventos = []
participantes = []
inscricoes = []
```

Por esse motivo, ao encerrar ou reiniciar o servidor, os dados cadastrados são apagados.

---

# Testes

Os testes da API podem ser realizados utilizando o Swagger:

```text
http://127.0.0.1:8000/docs
```

Principais cenários testados:

- cadastro de evento;
- consulta de eventos;
- atualização de evento;
- exclusão de evento;
- cadastro de participante;
- consulta de participantes;
- atualização de participante;
- exclusão de participante;
- inscrição em evento;
- tentativa de inscrição duplicada;
- tentativa de inscrição em evento sem vagas;
- busca de recurso inexistente;
- envio de dados inválidos.

---

# Autor

Phillipe Mugnaini

Projeto desenvolvido para a disciplina de Desenvolvimento Back-End.