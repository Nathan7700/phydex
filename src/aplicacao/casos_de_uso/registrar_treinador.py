from sqlalchemy.orm import Session
from src.infraestrutura.bd.modelos import TreinadorModelo
from src.infraestrutura.seguranca.criptografia import ServicoSeguranca
from src.apresentacao.schemas.auth_schemas import TreinadorCadastroSchema

class RegistrarTreinadorCasoDeUso:
    def __init__(self, db: Session):
        self.db = db

    def executar(self, dados: TreinadorCadastroSchema):
        # 1. Verificar se o email já existe
        treinador_existente = self.db.query(TreinadorModelo).filter(TreinadorModelo.email == dados.email).first()
        if treinador_existente:
            raise Exception("Este email já está registado.")

        # 2. Criptografar a senha
        senha_encriptada = ServicoSeguranca.gerar_hash_senha(dados.senha)

        # 3. Criar o modelo do banco
        novo_treinador = TreinadorModelo(
            nome=dados.nome,
            email=dados.email,
            senha_hash=senha_encriptada
        )

        # 4. Salvar no banco
        self.db.add(novo_treinador)
        self.db.commit()
        self.db.refresh(novo_treinador)
        
        return {"mensagem": "Treinador registrado com sucesso!"}