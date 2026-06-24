from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.infraestrutura.bd.sessao import obter_bd
from src.apresentacao.schemas.auth_schemas import TreinadorCadastroSchema, TreinadorLoginSchema, TokenSchema
from src.aplicacao.casos_de_uso.registrar_treinador import RegistrarTreinadorCasoDeUso
from src.aplicacao.casos_de_uso.autenticar_treinador import AutenticarTreinadorCasoDeUso
from src.infraestrutura.seguranca.autenticacao import obter_treinador_atual
from src.infraestrutura.bd.modelos import TreinadorModelo

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/signup", status_code=status.HTTP_201_CREATED)
def cadastrar_treinador(dados: TreinadorCadastroSchema, db: Session = Depends(obter_bd)):
    try:
        caso_de_uso = RegistrarTreinadorCasoDeUso(db)
        return caso_de_uso.executar(dados)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/login", response_model=TokenSchema)
def login_treinador(dados: TreinadorLoginSchema, db: Session = Depends(obter_bd)):
    try:
        caso_de_uso = AutenticarTreinadorCasoDeUso(db)
        return caso_de_uso.executar(dados)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

@router.get("/perfil")
def ver_perfil(treinador_atual: TreinadorModelo = Depends(obter_treinador_atual)):
    return {
        "mensagem": f"Olá {treinador_atual.nome}! Você está em uma rota protegida.",
        "seu_email": treinador_atual.email,
        "seu_id": treinador_atual.id
    }