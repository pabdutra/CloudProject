import os
import yfinance as yf
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from argon2 import PasswordHasher
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from models import Token, User, Base

# Configurações do JWT
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# Configurações de segurança para hashing de senha
ph = PasswordHasher()

# Configurações do banco de dados
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://projeto:projeto@db:5432/projeto')
engine = create_engine(DATABASE_URL)
# Cria as tabelas no banco de dados, se não existirem
Base.metadata.create_all(bind=engine)
# Cria a sessão do banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Função para criar hash de senha
def get_password_hash(password):
    return ph.hash(password)

# Função para verificar senha
def verify_password(plain_password, hashed_password):
    try:
        return ph.verify(hashed_password, plain_password)
    except:
        return False

# Função para gerar ou reutilizar token de acesso
def create_or_reuse_access_token(user_email: str, db: Session, expires_delta: timedelta = None):
    expiration_time = datetime.now(timezone.utc) + expires_delta if expires_delta else datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Tenta encontrar um token existente e válido para o usuário
    existing_token = db.query(Token).join(User).filter(
        User.email == user_email,
        Token.expires_at > datetime.now(timezone.utc)
    ).first()
    
    # Reutiliza o token se existir e estiver válido
    if existing_token:
        return existing_token.token

    # Caso contrário, cria um novo token
    data = {"sub": user_email, "exp": expiration_time}
    new_token_str = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    # Obtém o usuário pelo email
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise ValueError("Usuário não encontrado")

    # Salva o novo token no banco de dados
    new_token = Token(user_id=user.id, token=new_token_str, expires_at=expiration_time)
    db.add(new_token)
    db.commit()
    
    return new_token_str

from fastapi import HTTPException

def verify_bearer_token_format(authorization: str):
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=403, 
            detail="Token inválido: Siga o formato aceito 'Bearer <JWT_valido>'."
        )
    return authorization.replace("Bearer ", "")  # Retorna apenas o token

# Função para decodificar e verificar o token JWT
def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise ValueError("JWT inválido ou expirado.")

# Dependência para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Função para consultar a cotação
def consultar_cotacao(ticker, num_days_needed=10):
    end_date = datetime.now()
    results = []
    current_date = end_date

    while len(results) < num_days_needed:
        data = yf.download(ticker, start=current_date.strftime('%Y-%m-%d'),
                           end=(current_date + timedelta(days=1)).strftime('%Y-%m-%d'),
                           interval='1d')

        if not data.empty:
            row = data.iloc[0]  # Pega a primeira linha se houver dados
            results.append({
                'data': current_date.strftime('%Y-%m-%d'),
                'maximo': round(row['High'], 4),       # Limita a 3 casas decimais
                'minimo': round(row['Low'], 4),        # Limita a 3 casas decimais
                'fechamento': round(row['Close'], 4),  # Limita a 3 casas decimais
            })

        current_date -= timedelta(days=1)
    
    return results
