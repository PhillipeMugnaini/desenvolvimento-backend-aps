# APS 3 | API de Eventos Acadêmicos

API RESTful desenvolvida em Python com FastAPI, SQLite, SQLAlchemy ORM e Pydantic para gerenciamento de eventos acadêmicos, participantes, inscrições e geração de relatórios consolidados.

Projeto desenvolvido para a Avaliação Parcial 03 (APS 3) da disciplina de Desenvolvimento Back-End, dando continuidade à API implementada na APS 2.

## 1. Sobre o projeto

A aplicação simula um sistema de gerenciamento de eventos de uma instituição de ensino, permitindo administrar palestras, workshops, minicursos, seminários e outras atividades acadêmicas.

Na APS 2, os dados eram armazenados em listas Python, sendo perdidos quando a aplicação era encerrada.

Na APS 3, esse armazenamento foi substituído por um banco de dados SQLite, utilizando SQLAlchemy ORM para realizar as operações de persistência.

O sistema oferece:

- CRUD completo de eventos e participantes;
- Inscrição de participantes em eventos;
- Verificação de disponibilidade de vagas;
- Prevenção de inscrições duplicadas;
- Validação de dados e e-mails;
- Controle de integridade referencial;
- Persistência dos dados entre execuções;
- Relatórios dinâmicos de ocupação, categorias e participação por curso;
- Documentação interativa por meio do Swagger UI.

## 2. Tecnologias utilizadas

| Tecnologia | Finalidade |
|---|---|
| Python | Linguagem principal |
| FastAPI | Desenvolvimento da API REST |
| SQLite | Banco de dados relacional |
| SQLAlchemy ORM | Mapeamento das entidades e acesso ao banco |
| Pydantic | Validação de entradas e respostas |
| Uvicorn | Servidor ASGI |
| Swagger UI | Documentação e testes das rotas |
| Git e GitHub | Versionamento do código |

As dependências e suas respectivas versões estão registradas em `requirements.txt`.

## 3. Estrutura do projeto

```text
APS 3/
├── main.py
├── database.py
├── requirements.txt
├── README.md
│
├── controller/
│   ├── evento_controller.py
│   ├── participante_controller.py
│   ├── inscricao_controller.py
│   └── relatorio_controller.py
│
├── model/
│   ├── __init__.py
│   ├── evento.py
│   ├── participante.py
│   └── inscricao.py
│
├── schema/
│   ├── evento_schema.py
│   ├── participante_schema.py
│   └── inscricao_schema.py
│
└── service/
    ├── evento_service.py
    ├── participante_service.py
    ├── inscricao_service.py
    └── relatorio_service.py
```

O arquivo `eventos.db` é criado localmente durante a inicialização do banco de dados e não precisa ser versionado.

O ambiente virtual `.venv/` também é criado localmente e não deve ser enviado ao repositório.

## 4. Arquitetura da aplicação

O projeto utiliza uma arquitetura baseada em MVC, com separação adicional das regras de negócio em uma camada Service.

### Model

Representa as entidades e os relacionamentos do banco de dados, utilizando SQLAlchemy ORM.

### Schema

Define a estrutura dos dados de entrada e saída da API, utilizando Pydantic para validação.

### Controller

Recebe as requisições HTTP, chama os serviços correspondentes e retorna as respostas com os códigos HTTP apropriados.

### Service

Contém as regras de negócio, validações, consultas ao banco e operações CRUD.

### Database

Centraliza a configuração da conexão SQLite, a criação das sessões SQLAlchemy e o gerenciamento dos recursos de acesso ao banco.

### Fluxo de funcionamento

```text
Cliente / Swagger UI
         |
         v
Controller (FastAPI)
         |
         v
Schema (Pydantic)
         |
         v
Service (Regras de negócio)
         |
         v
SQLAlchemy ORM
         |
         v
SQLite (eventos.db)
```

## 5. Instalação e configuração

### Pré-requisitos

- Python instalado, preferencialmente versão 3.14;
- Git;
- Terminal Linux ou Windows;
- VS Code ou outro editor de código.

### 5.1. Clonar o repositório

```bash
git clone https://github.com/PhillipeMugnaini/desenvolvimento-backend-aps.git
```

Acessar a pasta da APS 3:

```bash
cd desenvolvimento-backend-aps
cd "APS 3"
```

### 5.2. Criar o ambiente virtual

No Linux/Fedora:

```bash
python3 -m venv .venv
```

Ativar:

```bash
source .venv/bin/activate
```

No Windows (PowerShell):

```powershell
python -m venv .venv
```

Ativar:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5.3. Instalar as dependências

Com o ambiente virtual ativado:

```bash
python -m pip install -r requirements.txt
```

Caso haja problemas com o índice de pacotes, utilize o PyPI oficial:

```bash
python -m pip install --index-url https://pypi.org/simple -r requirements.txt
```

### 5.4. Inicializar o banco de dados

A aplicação utiliza SQLite, portanto não é necessário instalar um servidor de banco de dados separadamente.

Antes da primeira execução, crie as tabelas por meio dos modelos SQLAlchemy:

```bash
python -c "import model; from database import Base, engine; Base.metadata.create_all(bind=engine); print('Tabelas inicializadas!')"
```

O comando cria as tabelas que ainda não existem:

- `eventos`
- `participantes`
- `inscricoes`

O arquivo `eventos.db` será armazenado na pasta `APS 3`.

A operação `create_all()` cria tabelas ausentes, mas não realiza migrações de alterações em tabelas existentes.

## 6. Executando a aplicação

Dentro da pasta `APS 3`, com o ambiente virtual ativado, execute:

```bash
python -m uvicorn main:app --reload
```

A API estará disponível em:

http://127.0.0.1:8000

A documentação interativa Swagger estará disponível em:

http://127.0.0.1:8000/docs

O endpoint raiz:

```http
GET /
```

Retorna:

```json
{
  "mensagem": "API de Eventos Acadêmicos funcionando!"
}
```

Para interromper o servidor, pressione `Ctrl + C` no terminal.

## 7. Modelagem do banco de dados

A aplicação utiliza três entidades relacionadas.

### Evento

| Campo | Descrição |
|---|---|
| id | Identificador único |
| titulo | Título do evento |
| descricao | Descrição do evento |
| data | Data de realização |
| horario | Horário do evento |
| local | Local de realização |
| capacidade | Quantidade máxima de participantes |
| categoria | Categoria do evento |

### Participante

| Campo | Descrição |
|---|---|
| id | Identificador único |
| nome | Nome do participante |
| email | E-mail único |
| curso | Curso do participante |

### Inscrição

| Campo | Descrição |
|---|---|
| id | Identificador único |
| evento_id | Chave estrangeira do evento |
| participante_id | Chave estrangeira do participante |
| data_inscricao | Data e horário da inscrição |

### Relacionamentos

- Um evento pode possuir várias inscrições.
- Um participante pode realizar inscrições em diferentes eventos.
- Cada inscrição pertence a um único evento e a um único participante.
- A combinação de `evento_id` e `participante_id` possui restrição de unicidade.

Os relacionamentos são implementados utilizando `ForeignKey`, `relationship()` e `UniqueConstraint` do SQLAlchemy.

## 8. Endpoints da API

### 8.1. Eventos

| Método | Endpoint | Descrição |
|---|---|---|
| POST | `/eventos` | Cadastrar evento |
| GET | `/eventos` | Listar eventos |
| GET | `/eventos/{evento_id}` | Consultar evento |
| PUT | `/eventos/{evento_id}` | Atualizar evento |
| DELETE | `/eventos/{evento_id}` | Excluir evento |

Exemplo de cadastro:

```http
POST /eventos
```

```json
{
  "titulo": "Workshop de Python",
  "descricao": "Introdução à programação em Python",
  "data": "2026-12-15",
  "horario": "14:00:00",
  "local": "Laboratório 1",
  "capacidade": 30,
  "categoria": "Workshop"
}
```

Resposta de sucesso: `201 Created`.

Os registros ficam armazenados no SQLite e podem ser consultados após reiniciar a aplicação.

### 8.2. Participantes

| Método | Endpoint | Descrição |
|---|---|---|
| POST | `/participantes` | Cadastrar participante |
| GET | `/participantes` | Listar participantes |
| GET | `/participantes/{participante_id}` | Consultar participante |
| PUT | `/participantes/{participante_id}` | Atualizar participante |
| DELETE | `/participantes/{participante_id}` | Excluir participante |

Exemplo de cadastro:

```http
POST /participantes
```

```json
{
  "nome": "João Silva",
  "email": "joao@email.com",
  "curso": "Engenharia de Software"
}
```

Resposta de sucesso: `201 Created`.

O sistema impede cadastros com e-mails duplicados e valida o formato do endereço eletrônico.

### 8.3. Inscrições

| Método | Endpoint | Descrição |
|---|---|---|
| POST | `/eventos/{evento_id}/inscricoes/{participante_id}` | Inscrever participante |
| GET | `/eventos/{evento_id}/inscricoes` | Listar inscritos no evento |

Exemplo:

```http
POST /eventos/1/inscricoes/1
```

Resposta ilustrativa:

```json
{
  "id": 1,
  "evento_id": 1,
  "participante_id": 1,
  "data_inscricao": "2026-11-17T12:00:00"
}
```

O identificador e a data são gerados pela aplicação.

Antes de cadastrar uma inscrição, a API verifica:

1. Se o evento existe;
2. Se o participante existe;
3. Se a inscrição já foi realizada;
4. Se existem vagas disponíveis.

Uma tentativa de inscrição duplicada ou em evento lotado retorna HTTP `409 Conflict`.

## 9. Relatórios e consolidação de dados

Os relatórios são construídos com consultas SQLAlchemy e apresentam resultados calculados dinamicamente, utilizando os registros existentes no SQLite.

### 9.1. Ocupação dos eventos

```http
GET /relatorios/eventos/ocupacao
```

Apresenta, para cada evento:

- Identificador e título;
- Capacidade total;
- Total de inscritos;
- Vagas disponíveis;
- Percentual de ocupação.

Fórmula:

```text
Percentual = (Total de inscritos / Capacidade) × 100
```

Exemplo ilustrativo:

```json
[
  {
    "evento_id": 1,
    "titulo": "Workshop de Python",
    "capacidade": 30,
    "total_inscritos": 15,
    "vagas_disponiveis": 15,
    "percentual_ocupacao": 50.0
  }
]
```

O relatório utiliza `OUTER JOIN` para incluir eventos sem inscrições e trata a divisão por zero.

### 9.2. Eventos por categoria

```http
GET /relatorios/eventos/categorias
```

Apresenta:

- Categoria;
- Quantidade de eventos;
- Capacidade total;
- Quantidade total de inscrições.

Exemplo ilustrativo:

```json
[
  {
    "categoria": "Workshop",
    "total_eventos": 3,
    "capacidade_total": 90,
    "total_inscricoes": 45
  }
]
```

A consolidação utiliza agrupamentos e subconsultas para evitar a contagem incorreta dos eventos e de suas capacidades.

### 9.3. Participação por curso

```http
GET /relatorios/participantes/cursos
```

Apresenta:

- Nome do curso;
- Total de participantes cadastrados;
- Total de inscrições realizadas.

Exemplo ilustrativo:

```json
[
  {
    "curso": "Engenharia de Software",
    "total_participantes": 20,
    "total_inscricoes": 35
  }
]
```

O relatório evita a duplicação da quantidade de participantes quando um mesmo aluno possui inscrições em vários eventos.

Também considera participantes sem inscrições.

## 10. Validação e integridade dos dados

A aplicação utiliza Pydantic e as restrições do SQLAlchemy para validar informações e preservar os relacionamentos.

Entre as regras implementadas estão:

- O título do evento não pode ser vazio;
- O nome do participante não pode ser vazio;
- O e-mail deve possuir um formato válido;
- A capacidade do evento deve ser maior que zero;
- As datas e horários devem possuir formatos válidos;
- Os campos obrigatórios devem ser informados;
- Um e-mail não pode pertencer a dois participantes;
- Um participante não pode se inscrever duas vezes no mesmo evento;
- Uma inscrição exige evento e participante existentes;
- Não são permitidas inscrições acima da capacidade;
- A capacidade não pode ser reduzida abaixo da quantidade de inscritos.

O SQLite utiliza a configuração `PRAGMA foreign_keys=ON` para ativar a verificação de chaves estrangeiras nas conexões.

Os relacionamentos ORM também possuem regras de exclusão em cascata para remover inscrições relacionadas quando eventos ou participantes são excluídos pelo SQLAlchemy.

## 11. Tratamento de erros HTTP

| Código | Significado | Exemplo |
|---|---|---|
| 200 | OK | Consulta ou atualização realizada |
| 201 | Created | Cadastro ou inscrição realizada |
| 204 | No Content | Registro excluído |
| 404 | Not Found | Evento ou participante inexistente |
| 409 | Conflict | E-mail duplicado, inscrição duplicada ou ausência de vagas |
| 422 | Unprocessable Entity | Dados inválidos |

Exemplo de resposta para e-mail duplicado:

```json
{
  "detail": "Já existe um participante cadastrado com este e-mail."
}
```

Exemplo de resposta para evento lotado:

```json
{
  "detail": "Não existem vagas disponíveis para este evento."
}
```

## 12. Testes e validação

Os testes funcionais são realizados manualmente utilizando o Swagger UI.

### 12.1. Testes de eventos

1. Cadastrar um evento;
2. Listar eventos;
3. Buscar evento pelo ID;
4. Atualizar um evento;
5. Excluir um evento;
6. Consultar um evento inexistente.

### 12.2. Testes de participantes

1. Cadastrar participante;
2. Consultar participante;
3. Atualizar participante;
4. Excluir participante;
5. Tentar cadastrar e-mail duplicado;
6. Tentar cadastrar e-mail inválido.

### 12.3. Testes de inscrições

1. Inscrever participante em evento;
2. Consultar inscritos;
3. Tentar inscrição duplicada;
4. Tentar inscrição em evento inexistente;
5. Tentar inscrição de participante inexistente;
6. Tentar inscrição em evento sem vagas;
7. Verificar exclusões com registros relacionados.

### 12.4. Teste de persistência

1. Cadastrar um evento e um participante;
2. Encerrar o servidor com `Ctrl + C`;
3. Iniciar novamente a API;
4. Consultar os registros por meio das rotas GET;
5. Confirmar que os dados permanecem disponíveis.

### 12.5. Testes dos relatórios

1. Consultar o relatório de ocupação;
2. Conferir eventos sem inscrições;
3. Consultar o relatório por categoria;
4. Verificar a soma das capacidades;
5. Consultar o relatório por curso;
6. Confirmar a contagem de participantes sem duplicação;
7. Inserir novos registros e verificar se os totais são atualizados.

### 12.6. Verificação das chaves estrangeiras

Com o ambiente virtual ativado, execute:

```bash
python - <<'PY'
from database import engine

with engine.connect() as conexao:
    ativo = conexao.exec_driver_sql(
        "PRAGMA foreign_keys"
    ).scalar()

    problemas = conexao.exec_driver_sql(
        "PRAGMA foreign_key_check"
    ).fetchall()

    print("Chaves estrangeiras:", ativo)
    print("Problemas de integridade:", problemas)
PY
```

Resultado esperado em um banco consistente:

```text
Chaves estrangeiras: 1
Problemas de integridade: []
```

## 13. Persistência e armazenamento

O projeto utiliza o SQLite por ser um banco de dados relacional leve, integrado à aplicação e que não exige um servidor separado.

O arquivo utilizado é:

```text
APS 3/eventos.db
```

As operações de leitura e escrita são realizadas por meio de sessões SQLAlchemy.

Os dados permanecem armazenados após o encerramento ou reinicialização da API.

O banco de dados é local e não é necessário enviá-lo ao GitHub. Cada ambiente pode criar suas próprias tabelas utilizando o comando documentado na seção de instalação.

## 14. Documentação da API

O FastAPI gera automaticamente a documentação OpenAPI.

Swagger UI:

http://127.0.0.1:8000/docs

Especificação OpenAPI em JSON:

http://127.0.0.1:8000/openapi.json

O Swagger permite visualizar os endpoints, enviar requisições, informar parâmetros e consultar os códigos de resposta.

## 15. Repositório

O código-fonte está disponível em:

[GitHub - Desenvolvimento Back-End APS](https://github.com/PhillipeMugnaini/desenvolvimento-backend-aps)

A pasta `APS 3` contém a API de eventos acadêmicos desenvolvida nesta avaliação.

## 16. Autor

Phillipe Mugnaini

Engenharia de Software

Projeto acadêmico desenvolvido para a disciplina de Desenvolvimento Back-End.

[Perfil no GitHub](https://github.com/PhillipeMugnaini)