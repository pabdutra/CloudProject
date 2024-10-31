from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from utils import (
    consultar_cotacao, create_or_reuse_access_token, get_db, get_password_hash, verify_password, decode_token, verify_bearer_token_format
)
from models import User

# Definir o esquema de segurança com APIKeyHeader
api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

app = FastAPI()

# Endpoint para registrar um usuário
@app.post("/registrar")
def registrar(nome: str, email: str, senha: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if user:
        raise HTTPException(status_code=409, detail="Email já registrado")
    
    hashed_password = get_password_hash(senha)
    new_user = User(nome=nome, email=email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = create_or_reuse_access_token(user_email=new_user.email, db=db)
    return {"jwt": access_token}

# Endpoint para fazer login
@app.post("/login")
def login(email: str, senha: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(senha, user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    access_token = create_or_reuse_access_token(user_email=user.email, db=db)
    return {"jwt": access_token}

# Endpoint para consultar a cotação do Euro/BRL nos últimos 10 dias
@app.get("/consultar")
def consultar(authorization: str = Depends(api_key_header), db: Session = Depends(get_db)):
    # Verifica se o token foi fornecido
    if not authorization:
        raise HTTPException(status_code=403, detail="Token de autenticação não fornecido.")
    
    # Verifica e obtém o token
    token = verify_bearer_token_format(authorization)
    
    try:
        # Decodifica o token para verificar sua validade
        decode_token(token)
    except Exception as e:
        raise HTTPException(status_code=401, detail="Token inválido: " + str(e))

    ticker = "EURBRL=X"
    try:
        results = consultar_cotacao(ticker)
        if not results:
            raise HTTPException(status_code=404, detail="Nenhum dado encontrado.")
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
