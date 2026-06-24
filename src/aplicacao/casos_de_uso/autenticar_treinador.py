from sqlalchemy.orm import Session
from src.infraestrutura.bd.modelos import TreinadorModelo
from src.infraestrutura.seguranca.criptografia import ServicoSeguranca
from src.apresentacao.schemas.auth_schemas import TreinadorLoginSchema

class AutenticarTreinadorCasoDeUso:
    def __init__(self, db: Session):
        self.db = db

    def executar(self, dados: TreinadorLoginSchema):
        # 1. Buscar o treinador pelo email
        treinador = self.db.query(TreinadorModelo).filter(TreinadorModelo.email == dados.email).first()
        if not treinador:
            raise Exception("Email ou senha incorretos.")

        # 2. Verificar se a senha está correta
        senha_correta = ServicoSeguranca.verificar_senha(dados.senha, treinador.senha_hash)
        if not senha_correta:
            raise Exception("Email ou senha incorretos.")

        # 3. Gerar o Token JWT colocando o ID do treinador lá dentro
        token = ServicoSeguranca.criar_token_acesso(dados={"sub": str(treinador.id)})

        return {"access_token": token, "token_type": "bearer"}