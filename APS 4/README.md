# APS 4 | API de Eventos Acadêmicos

API RESTful desenvolvida em Python com FastAPI para gerenciamento de eventos acadêmicos, participantes e inscrições. Esta etapa amplia a APS 3 com cadastro de usuários, autenticação JWT, armazenamento seguro de senhas e controle de acesso por perfis (RBAC).

Projeto da unidade curricular de Desenvolvimento Backend.

## Tecnologias

- Python 3.14 (ambiente utilizado no desenvolvimento)
- FastAPI e Uvicorn
- SQLite e SQLAlchemy ORM
- Pydantic (validação de entradas e respostas)
- `pwdlib[argon2]` (hash e verificação de senhas)
- PyJWT (geração e validação de tokens)
- `python-dotenv` (configuração da chave secreta)

As versões específicas das dependências estão no `requirements.txt`.

## Funcionalidades

- CRUD de eventos e participantes, preservado da APS 3.
- Inscrição de participantes em eventos, com verificações de existência, capacidade e duplicidade.
- Relatórios de ocupação, eventos por categoria e participações por curso.
- Cadastro de usuários com perfil padrão `usuario`.
- Senhas armazenadas exclusivamente como hash Argon2.
- Login por e-mail e senha, com retorno de JWT assinado.
- Consulta do perfil autenticado em `GET /auth/me`.
- Autorização de rotas com os perfis `usuario` e `administrador`.
- Respostas HTTP apropriadas para falhas de autenticação, permissão e validação.

## Estrutura do projeto

```text
APS 4/
├── controller/
│   ├── auth_controller.py
│   ├── evento_controller.py
│   ├── inscricao_controller.py
│   ├── participante_controller.py
│   ├── relatorio_controller.py
│   └── usuario_controller.py
├── model/
│   ├── __init__.py
│   ├── evento.py
│   ├── inscricao.py
│   ├── participante.py
│   └── usuario.py
├── schema/
│   ├── auth_schema.py
│   ├── evento_schema.py
│   ├── inscricao_schema.py
│   ├── participante_schema.py
│   └── usuario_schema.py
├── service/
│   ├── auth_service.py
│   ├── evento_service.py
│   ├── inscricao_service.py
│   ├── participante_service.py
│   ├── relatorio_service.py
│   └── usuario_service.py
├── security/
│   ├── __init__.py
│   ├── dependencies.py
│   ├── jwt.py
│   └── password.py
├── scripts/
│   ├── __init__.py
│   └── criar_admin.py
├── .env.example
├── .gitignore
├── database.py
├── main.py
├── requirements.txt
└── README.md
```

O banco `eventos.db`, o arquivo `.env` e a pasta `.venv/` são gerados localmente e não devem ser versionados.

### Separação de responsabilidades

| Camada | Responsabilidade |
| --- | --- |
| `controller/` | Definição dos endpoints, requisições e respostas HTTP. |
| `schema/` | Validação de dados de entrada e serialização das respostas com Pydantic. |
| `service/` | Regras de negócio e operações da aplicação. |
| `model/` | Entidades e relacionamentos do SQLAlchemy. |
| `security/` | Hash de senhas, JWT e dependências de autenticação/autorização. |
| `database.py` | Conexão com o SQLite e gerenciamento das sessões. |
| `scripts/` | Inicialização local e controlada do administrador. |

## Instalação e execução

Os comandos abaixo são para Linux (incluindo Fedora), a partir de um terminal com Python e Git instalados.

### 1. Clonar o repositório

```bash
git clone https://github.com/PhillipeMugnaini/desenvolvimento-backend-aps.git
cd "desenvolvimento-backend-aps/APS 4"
```

As aspas são necessárias porque o nome da pasta contém um espaço.

### 2. Criar e ativar o ambiente virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### 3. Configurar a chave JWT

O arquivo `.env.example` descreve a variável `JWT_SECRET_KEY`, mas não possui uma chave real. Gere um arquivo `.env` exclusivo para sua máquina:

```bash
python - <<'PY'
from pathlib import Path
import secrets

arquivo = Path('.env')
if arquivo.exists():
    raise SystemExit('O arquivo .env já existe; nenhuma chave foi alterada.')

arquivo.write_text('JWT_SECRET_KEY=' + secrets.token_hex(32) + '\n', encoding='utf-8')
arquivo.chmod(0o600)
print('Configuração JWT criada.')
PY
```

Não compartilhe nem versione o `.env`. A aplicação usa o algoritmo `HS256` e tokens válidos por 30 minutos. Um token expirado exige novo login.

### 4. Inicializar as tabelas do banco

Na primeira execução, crie as tabelas do SQLAlchemy, incluindo `usuarios`:

```bash
python - <<'PY'
import model
from database import Base, engine

Base.metadata.create_all(bind=engine)
print('Banco SQLite inicializado.')
PY
```

Isso gera `eventos.db` localmente. O comando `create_all()` cria tabelas ausentes, mas não realiza migrações de tabelas já existentes.

### 5. Criar o administrador inicial

```bash
python -m scripts.criar_admin
```

Informe nome, e-mail e senha forte quando solicitado. A senha é recebida sem eco no terminal e armazenada como hash Argon2. O script só permite a criação inicial quando ainda não existe administrador. Não há cadastro público de administradores.

### 6. Iniciar a API

```bash
python -m uvicorn main:app --reload
```

- Documentação Swagger: http://127.0.0.1:8000/docs
- Especificação OpenAPI: http://127.0.0.1:8000/openapi.json
- Rota inicial: http://127.0.0.1:8000/

O argumento `--reload` é indicado para desenvolvimento local.

## Segurança e autenticação

### Cadastro público

`POST /usuarios` cria uma conta sempre com perfil `usuario`. O cliente informa nome, e-mail válido e senha com 8 a 128 caracteres. Campos extras, como `perfil`, são rejeitados; e-mails duplicados resultam em HTTP `409`.

Exemplo de requisição:

```http
POST /usuarios
Content-Type: application/json
```

```json
{
  "nome": "Aluno Exemplo",
  "email": "aluno@exemplo.com",
  "senha": "SenhaForte123!"
}
```

Exemplo de resposta (`201 Created`):

```json
{
  "id": 1,
  "nome": "Aluno Exemplo",
  "email": "aluno@exemplo.com",
  "perfil": "usuario"
}
```

Senha e hash não são incluídos na resposta.

### Login

`POST /auth/login` verifica as credenciais com Argon2 e retorna um JWT.

```json
{
  "email": "aluno@exemplo.com",
  "senha": "SenhaForte123!"
}
```

Resposta (`200 OK`):

```json
{
  "access_token": "<JWT_ASSINADO>",
  "token_type": "bearer"
}
```

O token carrega o identificador do usuário (`sub`), a data de emissão (`iat`) e a expiração (`exp`), sem incluir senha ou hash. O servidor verifica a assinatura, a expiração e a existência do usuário no banco.

### Acesso com token

Nas rotas protegidas, envie o cabeçalho HTTP:

```http
Authorization: Bearer <JWT_ASSINADO>
```

No Swagger, execute o login, copie o valor de `access_token` e informe-o no botão **Authorize** (sem adicionar manualmente o texto `Bearer`).

`GET /auth/me` retorna o usuário correspondente ao token:

```json
{
  "id": 1,
  "nome": "Aluno Exemplo",
  "email": "aluno@exemplo.com",
  "perfil": "usuario"
}
```

## Rotas e permissões

Legenda: **Pública** = sem login; **Autenticado** = qualquer perfil com JWT válido; **Administrador** = perfil `administrador` com JWT válido.

| Método | Rota | Acesso |
| --- | --- | --- |
| GET | `/` | Pública |
| POST | `/usuarios` | Pública (sempre cria `usuario`) |
| POST | `/auth/login` | Pública |
| GET | `/auth/me` | Autenticado |
| GET | `/eventos` | Pública |
| GET | `/eventos/{evento_id}` | Pública |
| POST | `/eventos` | Administrador |
| PUT | `/eventos/{evento_id}` | Administrador |
| DELETE | `/eventos/{evento_id}` | Administrador |
| GET | `/participantes` | Autenticado |
| GET | `/participantes/{participante_id}` | Autenticado |
| POST | `/participantes` | Administrador |
| PUT | `/participantes/{participante_id}` | Administrador |
| DELETE | `/participantes/{participante_id}` | Administrador |
| POST | `/eventos/{evento_id}/inscricoes/{participante_id}` | Autenticado |
| GET | `/eventos/{evento_id}/inscricoes` | Administrador |
| GET | `/relatorios/eventos/ocupacao` | Administrador |
| GET | `/relatorios/eventos/categorias` | Administrador |
| GET | `/relatorios/participantes/cursos` | Administrador |

O servidor verifica os perfis usando dependências FastAPI (`obter_usuario_atual` e `exigir_administrador`), não dados de perfil informados pelo cliente.

### Regras de negócio preservadas da APS 3

- Eventos possuem título, descrição, data, horário, local, capacidade e categoria.
- A capacidade deve ser positiva; reduzi-la abaixo do número atual de inscritos é impedido.
- Participantes possuem nome, e-mail único e curso.
- Inscrições exigem evento e participante existentes, não podem ser duplicadas e respeitam o limite de vagas.
- A exclusão de registros segue os relacionamentos e as regras já implementadas no SQLite/SQLAlchemy.

**Limitação conhecida:** contas de acesso (`usuarios`) e participantes de eventos (`participantes`) não têm vínculo de titularidade. Assim, uma conta autenticada pode inscrever um `participante_id` existente. Essa é a regra adotada nesta avaliação; um sistema de produção exigiria verificação de titularidade ou autorização adicional.

## Relatórios

Os três relatórios, herdados da APS 3, exigem administrador:

- `GET /relatorios/eventos/ocupacao`: ocupação e inscrições dos eventos.
- `GET /relatorios/eventos/categorias`: consolidação de eventos por categoria.
- `GET /relatorios/participantes/cursos`: participação agrupada por curso.

A lógica de cálculo desses relatórios foi preservada.

## Códigos HTTP

| Código | Situação |
| --- | --- |
| `200 OK` | Consulta, login ou atualização realizada com sucesso. |
| `201 Created` | Cadastro ou inscrição criada com sucesso. |
| `204 No Content` | Exclusão realizada com sucesso. |
| `401 Unauthorized` | Credenciais inválidas, token ausente, inválido ou expirado. |
| `403 Forbidden` | Usuário autenticado sem a permissão necessária. |
| `404 Not Found` | Registro solicitado não encontrado. |
| `409 Conflict` | E-mail duplicado, inscrição duplicada, evento sem vagas ou conflito de integridade. |
| `422 Unprocessable Entity` | Corpo da requisição inválido conforme as validações Pydantic. |

Para evitar enumeração de contas, o login responde com a mesma mensagem genérica quando o e-mail não existe ou a senha está incorreta.

## Como reproduzir os testes no Swagger

Acesse `/docs` com a aplicação em execução. Tenha um administrador criado pelo script e um usuário comum cadastrado em `POST /usuarios`.

| Cenário | Procedimento | Resultado esperado |
| --- | --- | --- |
| Cadastro de usuário | `POST /usuarios` com dados válidos | `201`, sem senha/hash na resposta |
| E-mail duplicado | Repetir o cadastro | `409` |
| Perfil indevido | Enviar `perfil: administrador` no cadastro público | `422` |
| Senha em hash | Inspecionar `usuarios.senha_hash` localmente sem divulgar valor | Hash Argon2, não senha original |
| Login válido | `POST /auth/login` com credenciais corretas | `200` e JWT |
| Login inválido | Informar senha incorreta ou e-mail inexistente | `401` e mensagem genérica |
| Rota sem token | Tentar `POST /eventos` sem autenticação | `401` |
| Token inválido | Usar um token adulterado em `/auth/me` | `401` |
| Token expirado | Usar JWT com `exp` no passado | `401` |
| Usuário comum | Tentar `POST /eventos` com JWT comum | `403` |
| Administrador | Criar evento usando JWT de administrador | `201` |
| Meu perfil | `GET /auth/me` com JWT válido | `200`, dados do próprio usuário |
| Inscrições | Inscrever participante duas vezes no mesmo evento | `201` e depois `409` |
| Relatórios | Consultar com JWT de administrador | `200`, dados consolidados |
| Regressão | Testar CRUD e relatórios herdados da APS 3 | Mantêm as regras de negócio |

### Como conferir o hash sem revelar seu valor

No terminal, com o banco inicializado e pelo menos um usuário cadastrado:

```bash
python - <<'PY'
from sqlalchemy import select
from database import SessionLocal
from model import Usuario

with SessionLocal() as db:
    usuario = db.scalar(select(Usuario).limit(1))
    if usuario is None:
        print('Cadastre um usuário antes do teste.')
    else:
        print('Hash Argon2:', usuario.senha_hash.startswith('$argon2'))
PY
```

### Como testar um JWT expirado

Em uma instalação local, gere um token já expirado, usando a chave do próprio projeto:

```bash
python - <<'PY'
from datetime import datetime, timedelta, timezone
import jwt
from security.jwt import CHAVE_SECRETA, ALGORITMO

agora = datetime.now(timezone.utc)
token = jwt.encode(
    {'sub': '1', 'iat': agora - timedelta(hours=1),
     'exp': agora - timedelta(minutes=1)},
    CHAVE_SECRETA, algorithm=ALGORITMO
)
print(token)
PY
```

No Swagger, clique em **Authorize**, substitua o token pelo valor expirado e execute `GET /auth/me`. A resposta esperada é `401`. Não publique tokens reais nas evidências.

Registre capturas do Swagger mostrando requisição, código HTTP e resposta para comprovar os cenários da atividade.

## Cuidados com credenciais

- Nunca publique `.env`, `eventos.db`, tokens válidos ou senhas reais.
- `.env.example` é apenas um modelo, não deve conter segredo de verdade.
- Utilize senhas fortes e exclusivas para o administrador.
- Ao usar a aplicação fora do ambiente local de desenvolvimento, utilize HTTPS e revise o controle de identidade/titularidade de inscrições.

## Referências

- [Documentação do FastAPI](https://fastapi.tiangolo.com/)
- [Segurança com OAuth2 e JWT no FastAPI](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [Pydantic](https://docs.pydantic.dev/)
- [PyJWT](https://pyjwt.readthedocs.io/)
- [pwdlib](https://frankie567.github.io/pwdlib/)

## Repositório

[Desenvolvimento Backend - APS](https://github.com/PhillipeMugnaini/desenvolvimento-backend-aps)

A pasta `APS 3` contém a versão anterior da API; a pasta `APS 4` contém a evolução com autenticação e controle de permissões.
