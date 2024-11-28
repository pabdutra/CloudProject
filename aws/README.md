# Executando Aplicação Via AWS

Para visualizar a apresentação da API publicada na AWS via EKS, [clique aqui](https://alinsperedu-my.sharepoint.com/:v:/g/personal/pedroabd_al_insper_edu_br/Eab51V6KtG1Ek806k5SPa8kBPF10TUSl7mH2-pckPepvFQ).

## Acesso rápido para os arquivos de configuração do Kubernetes

+ [api-deployment.yaml](api-deployment.yaml)
+ [api-service.yaml](api-service.yaml)
+ [db-deployment.yaml](db-deployment.yaml)
+ [db-service.yaml](db-service.yaml)
+ [configmap.yaml](configmap.yaml)

## 0. Pré-requisitos

+ Tenha credenciais válidas para acessar o [console de gerenciamento da AWS](https://aws.amazon.com/pt/console/).

+ Siga o passo a passo [deste vídeo](https://www.youtube.com/watch?v=JrT5YV1KMeY) para criar e configurar corretamente seu EKS (Elastic Kubernetes Service).

## 1. Certifique-se de que o kubectl está configurado

O CloudShell já possui o AWS CLI configurado, mas pode ser necessário atualizar o `kubeconfig`:

```bash
aws eks update-kubeconfig --region <REGIAO> --name <NOME_DO_CLUSTER>
```

## 2. Envie os arquivos YAML para o CloudShell

Faça upload dos arquivos `api-deployment.yaml`, `api-service.yaml`, `db-deployment.yaml` e `db-service.yaml` no AWS CloudShell.

Caso opte por utilizar credenciais **próprias** para acessar o banco de dados, faça upload de `.env`.

Caso opte por utilizar credenciais **pradrão** para acessar o banco de dados, faça upload de `configmap.yaml`.

## 3. Aplique os arquivos

Caso tenha optado por utilizar credenciais **próprias** para acessar o banco de dados a partir do arquivo `.env`, execute:

```bash
kubectl create secret generic api-secrets --from-env-file=.env
```

Caso tenha optado por utilizar credenciais **pradrão** para acessar o banco de dados a partir do arquivo `configmap.yaml`, execute:

```bash
kubectl apply -f configmap.yaml
```

Ainda no AWS CloudShell, execute:

```bash
kubectl apply -f api-deployment.yaml
kubectl apply -f api-service.yaml
kubectl apply -f db-deployment.yaml
kubectl apply -f db-service.yaml
```

## 4. Verifique o status dos Pods e Serviços

Após aplicar os arquivos, você pode verificar o status dos pods e serviços com os seguintes comandos:

```bash
kubectl get pods
kubectl get services
```

## 5. Acesse a aplicação via navegador

Execute:

```bash
kubectl get all
```

Localize a o IP Externo e a porta utilizada para acessar a API pelo seu navegador.

## Links úteis relacionados

+ Para visualizar a apresentação da API publicada na AWS via EKS, [clique aqui](https://alinsperedu-my.sharepoint.com/:v:/g/personal/pedroabd_al_insper_edu_br/Eab51V6KtG1Ek806k5SPa8kBPF10TUSl7mH2-pckPepvFQ).
