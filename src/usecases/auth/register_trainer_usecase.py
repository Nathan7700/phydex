# src/usecases/auth/register_trainer_usecase.py
from src.adapters.schemas.auth_schemas import TrainerRegisterSchema
from src.domain.repositories.itrainer_repository import ITrainerRepository
from src.infrastructure.auth.crypto_service import CryptoService

class RegisterTrainerUseCase:
    """Business rule to register a new App User (Trainer) in the system."""

    # Inversão de dependência acontecendo no construtor
    def __init__(self, trainer_repo: ITrainerRepository):
        self.trainer_repo = trainer_repo

    def executar(self, dados: TrainerRegisterSchema) -> dict:
        # 1. Verifica se o e-mail já existe utilizando a abstração limpa
        email_existente = self.trainer_repo.obter_por_email(dados.email)

        if email_existente:
            raise Exception("Este e-mail já está cadastrado.")

        # 2. Criptografa a senha usando o serviço
        senha_criptografada = CryptoService.gerar_hash_senha(dados.password)

        # 3. Prepara o dicionário de dados de domínio puro
        dados_treinador = {
            "username": dados.name, # Mapeia o name recebido para o username do banco
            "email": dados.email,
            "password_hash": senha_criptografada
        }

        # 4. Salva usando a interface do repositório
        self.trainer_repo.salvar(dados_treinador)

        return {"mensagem": "Treinador cadastrado com sucesso!"}