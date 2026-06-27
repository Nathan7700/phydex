from datetime import datetime, timedelta, timezone
import bcrypt
import jwt

SECRET_KEY = "sua_chave_secreta_super_segura_aqui"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

class CryptoService:
    """Responsável por operações de hash de senha e geração de tokens JWT."""
    
    @staticmethod
    def gerar_hash_senha(senha: str) -> str:
        senha_bytes = senha.encode('utf-8')
        salt = bcrypt.gensalt()
        hash_bytes = bcrypt.hashpw(senha_bytes, salt)
        return hash_bytes.decode('utf-8')

    @staticmethod
    def verificar_senha(senha_pura: str, senha_hash: str) -> bool:
        return bcrypt.checkpw(senha_pura.encode('utf-8'), senha_hash.encode('utf-8'))

    @staticmethod
    def criar_token_acesso(dados: dict) -> str:
        dados_copia = dados.copy()
        tempo_expiracao = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        dados_copia.update({"exp": tempo_expiracao})
        token_jwt = jwt.encode(dados_copia, SECRET_KEY, algorithm=ALGORITHM)
        return token_jwt