from sqlalchemy.orm import Session

# Importações corrigidas alinhadas com a nova arquitetura em inglês
from src.adapters.schemas.auth_schemas import TrainerLoginSchema
from src.infrastructure.database.models.trainer_model import TrainerModel
from src.infrastructure.auth.crypto_service import CryptoService

class AuthenticateTrainerUseCase:
    """Regra de negócio para autenticar um usuário (Trainer) no aplicativo."""
    
    def __init__(self, db: Session):
        self.db = db

    def executar(self, dados: TrainerLoginSchema) -> dict:
        # 1. Busca o usuário (treinador do app) pelo e-mail
        usuario = self.db.query(TrainerModel).filter(TrainerModel.email == dados.email).first()
        
        if not usuario:
            raise Exception("Email ou senha incorretos.")

        # 2. Verifica se a senha pura bate com o hash salvo no banco de dados
        senha_correta = CryptoService.verificar_senha(dados.senha, usuario.senha_hash)
        
        # CORREÇÃO: Avalia a variável correta que foi declarada na linha de cima
        if not senha_correta:
            raise Exception("Email ou senha incorretos.")

        # 3. Gera o token de acesso vinculando o ID do usuário ao campo 'sub' do JWT
        token = CryptoService.criar_token_acesso({"sub": str(usuario.id)})
        
        return {
            "access_token": token, 
            "token_type": "bearer"
        }