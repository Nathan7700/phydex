from sqlalchemy.orm import Session
from src.adapters.schemas.auth_schemas import TrainerRegisterSchema
from src.infrastructure.database.models.trainer_model import TrainerModel
from src.infrastructure.auth.crypto_service import CryptoService

class RegisterTrainerUseCase:
    """Business rule to register a new App User (Trainer) in the system."""
    
    def __init__(self, db: Session):
        self.db = db

    def executar(self, dados: TrainerRegisterSchema) -> dict:
        # 1. Verifica se o e-mail já existe no banco de dados
        email_existente = self.db.query(TrainerModel).filter(
            TrainerModel.email == dados.email
        ).first()
        
        if email_existente:
            raise Exception("Este e-mail já está cadastrado.")

        # 2. Criptografa a senha usando o serviço de infraestrutura em inglês
        senha_criptografada = CryptoService.gerar_hash_senha(dados.password)

        # 3. Cria a nova instância do modelo físico de tabela
        novo_treinador = TrainerModel(
            nome=dados.name,
            email=dados.email,
            senha_hash=senha_criptografada
        )

        # 4. Salva no banco de dados
        self.db.add(novo_treinador)
        self.db.commit()
        self.db.refresh(novo_treinador)

        return {"mensagem": "Treinador cadastrado com sucesso!"}