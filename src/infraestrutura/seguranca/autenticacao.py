from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from sqlalchemy.orm import Session
from src.infraestrutura.bd.sessao import obter_bd
from src.infraestrutura.bd.modelos import TreinadorModelo
from src.infraestrutura.seguranca.criptografia import SECRET_KEY, ALGORITHM

# Esse componente ativa o botão de "Cadeado" (Authorize) no Swagger
security = HTTPBearer()

def obter_treinador_atual(
    credenciais: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(obter_bd)
) -> TreinadorModelo:
    
    token = credenciais.credentials
    erro_autenticacao = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou expirado.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decodifica o token JWT usando a chave secreta do projeto
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        treinador_id: str = payload.get("sub")
        
        if treinador_id is None:
            raise erro_autenticacao
            
    except jwt.PyJWTError:
        raise erro_autenticacao

    # Busca o treinador dono do token no banco de dados
    treinador = db.query(TreinadorModelo).filter(TreinadorModelo.id == int(treinador_id)).first()
    
    if treinador is None:
        raise erro_autenticacao
        
    # Retorna o objeto do treinador logado para a rota usar
    return treinador