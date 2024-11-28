# Executando Aplicação Via Docker

## 0. Pré-requisitos

+ Tenha o Docker instalado em seu sistema. Você pode baixar e instalar o Docker [aqui](https://www.docker.com/products/docker-desktop/).

+ Verifique se o Docker Compose está instalado. O Docker Desktop já inclui o Docker Compose.

+ Execute o Docker Desktop e deixe-o aberto em segundo plano.

## 1. Certifique-se de que `compose.yaml` está na raiz do projeto

O arquivo `compose.yaml` deve estar localizado na pasta principal do projeto, fora de subdiretórios. Ele é responsável por configurar os serviços necessários, como a API e o banco de dados PostgreSQL.

## 2. Crie o arquivo `.env`

No diretório raiz do projeto, crie um arquivo chamado `.env` e adicione as seguintes variáveis de ambiente, ajustando-as com suas credenciais Postgres e com os parämetros JWT desejados:

```plaintext
POSTGRES_DB = nome_da_base
POSTGRES_USER = seu_usuario_postgres
POSTGRES_PASSWORD = sua_senha_postgres
SECRET_KEY = senha_jwt
ALGORITHM  = HS256
ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

## 3. Construia e inicie os contêineres

Acesse o terminal na raiz do projeto, onde está o arquivo `compose.yaml`, e execute o seguinte comando:

```bash
docker-compose up -d
```

## 4. Acesse a API

A API estará disponível no endereço `http://localhost:8000`

## 5. Parar os contêineres

Quando terminar de usar a aplicação, você pode parar os contêineres com:

```bash
docker-compose down
```

## Links úteis relacionados

+ Para visualizar a execução da aplicação, [clique aqui](https://alinsperedu-my.sharepoint.com/:v:/g/personal/pedroabd_al_insper_edu_br/EeyWk-Hl75VFsGyRTEO_4HwB6JKctSVZpy4c-g6Eh_gvkA).

+ Para acessar o Docker Hub do projeto, [clique aqui](https://hub.docker.com/repository/docker/pedroabd/apicloud/general).
