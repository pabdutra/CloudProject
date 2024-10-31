# Utilizando uma imagem base oficial do Python
FROM python:3.11-slim

# Definindo o diretório de trabalho dentro do container
WORKDIR /app

# Copiando o arquivo requirements.txt para o container
COPY requirements.txt ./

# Instalando as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiando todo o código da aplicação para o container
COPY . .

# Expondo a porta 8000 para a API
EXPOSE 8000

# Comando para rodar a aplicação com o Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
