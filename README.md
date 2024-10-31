# API RESTful Dockerizada

>Computação em Nuvem - Projeto 2024.2

Por: Pedro Dutra

## Descrição

O projeto é uma API RESTful desenvolvida com FastAPI que permite aos usuários registrar-se, fazer login e consultar as 10 últimas cotações do Euro em relação ao Real (EUR/BRL). A API é protegida por autenticação baseada em JWT (JSON Web Tokens), garantindo que apenas usuários autenticados possam acessar as informações de cotação.

## Executando a aplicação

### 0. Pré-requisitos

+ Tenha o Docker instalado em seu sistema. Você pode baixar e instalar o Docker [aqui](https://www.docker.com/products/docker-desktop/).

+ Verifique se o Docker Compose está instalado. O Docker Desktop já inclui o Docker Compose.

+ Execute o Docker Desktop e deixe-o aberto em segundo plano.

### 1. Certifique-se de que `compose.yaml` está na raiz do projeto

O arquivo `compose.yaml` deve estar localizado na pasta principal do projeto, fora de subdiretórios. Ele é responsável por configurar os serviços necessários, como a API e o banco de dados PostgreSQL.

### 2. Crie o arquivo `.env`

No diretório raiz do projeto, crie um arquivo chamado `.env` e adicione as seguintes variáveis de ambiente, ajustando-as com suas credenciais Postgres e com os parämetros JWT desejados:

```plaintext
POSTGRES_DB = nome_da_base
POSTGRES_USER = seu_usuario_postgres
POSTGRES_PASSWORD = sua_senha_postgres
SECRET_KEY = senha_jwt
ALGORITHM  = HS256
ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

### 3. Construia e inicie os contêineres

Acesse o terminal na raiz do projeto, onde está o arquivo `compose.yaml`, e execute o seguinte comando:

```bash
docker-compose up -d
```

### 4. Acesse a API

A API estará disponível no endereço `http://localhost:8000`

### 5. Parar os contêineres

Quando terminar de usar a aplicação, você pode parar os contêineres com:

```bash
docker-compose down
```

## Documentação dos endpoints

### Registro de usuário

>URL: /registrar

Método POST que cria um novo usuário no sistema e gera seu token JWT.

#### Corpo da requisição

```json
{
    "nome": "usuario",
    "email": "usuario@dominio.com",
    "senha": "senha"
}
```

#### Respostas

+ **200 Successful Response**: Usuário criado com sucesso.

```json
{
    "jwt": "codigo_jwt"
}
```

+ **409 Conflict**: Erro de validação.

```json
{
  "detail": "Email já registrado"
}
```

### Login

>URL: /login

Método POST que autentica o usuário e retorna seu token JWT.

#### Corpo da requisição

```json
{
    "email": "usuario@dominio.com",
    "senha": "senha"
}
```

#### Respostas

+ **200 Successful Response**: Usuário autenticado com sucesso.

```json
{
    "jwt": "codigo_jwt"
}
```

+ **401 Unauthorized**: Usuário ou senha inválidos.

```json
{
  "detail": "Credenciais inválidas"
}
```

### Consulta de cotação

>URL: /consultar

Método GET que onsulta as 10 últimas cotações do Euro em relação ao Real. Requer autenticação via token JWT.

#### Autenticação

Cabeçalho `Authorization`: Deve conter o token JWT gerado no login ou registro, no formato `Bearer <token>`

#### Respostas

+ **200 Successful Response**: Retorna um JSON contendo a lista das cotações.

```json
[
  {
    "data": "2024-10-31",
    "maximo": {
      "EURBRL=X": 6.3047
    },
    "minimo": {
      "EURBRL=X": 6.2402
    },
    "fechamento": {
      "EURBRL=X": 6.3041
    }
  },
  ...
]
```

+ **401 Unauthorized**: Usuário ou senha inválidos.

```json
{
  "detail": "Token inválido: JWT inválido ou expirado."
}
```

+ **403 Forbidden**: Usuário ou senha inválidos.

```json
{
  "detail": "Token de autenticação não fornecido."
}
```

## Teste dos endpoints

### Registro de usuário

![Teste de registro de usuario.](/img/teste_registro.png)

### Login

![Teste de login.](/img/teste_login.png)

### Consulta de cotação

![Teste de consulta.](/img/teste_consulta.png)

## Links úteis

+ Para visualizar a execução da aplicação, [clique aqui](https://alinsperedu-my.sharepoint.com/:v:/g/personal/pedroabd_al_insper_edu_br/EeyWk-Hl75VFsGyRTEO_4HwB6JKctSVZpy4c-g6Eh_gvkA)

+ Para acessar o Docker Hub do projeto, [clique aqui](https://hub.docker.com/repository/docker/pedroabd/apicloud/general)
