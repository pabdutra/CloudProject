# API RESTful

>Computação em Nuvem - Projeto 2024.2

Por: Pedro Dutra

## Descrição

O projeto é uma API RESTful desenvolvida com FastAPI que permite aos usuários registrar-se, fazer login e consultar as 10 últimas cotações do Euro em relação ao Real (EUR/BRL). A API é protegida por autenticação baseada em JWT (JSON Web Tokens), garantindo que apenas usuários autenticados possam acessar as informações de cotação.

## Executando a aplicação

+ [Executando Aplicação Via Docker](docker/README.md) (Entrega Intermediária)

OU

+ [Executando Aplicação Via AWS](aws/README.md) (Entrega FInal)

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

+ **401 Unauthorized**: Token JWT inválido ou expirado.

```json
{
  "detail": "Token inválido: JWT inválido ou expirado."
}
```

+ **403 Forbidden**: Token JWT não fornecido.

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

+ Para visualizar a execução da aplicação, [clique aqui](https://alinsperedu-my.sharepoint.com/:v:/g/personal/pedroabd_al_insper_edu_br/EeyWk-Hl75VFsGyRTEO_4HwB6JKctSVZpy4c-g6Eh_gvkA).

+ Para acessar o Docker Hub do projeto, [clique aqui](https://hub.docker.com/repository/docker/pedroabd/apicloud/general).

+ Para visualizar a apresentação da API publicada na AWS via EKS, [clique aqui](https://alinsperedu-my.sharepoint.com/:v:/g/personal/pedroabd_al_insper_edu_br/Eab51V6KtG1Ek806k5SPa8kBPF10TUSl7mH2-pckPepvFQ).
