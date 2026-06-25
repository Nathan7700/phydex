from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.infraestrutura.bd.sessao import obter_bd
from src.infraestrutura.seguranca.autenticacao import obter_treinador_atual
from src.infraestrutura.bd.modelos import TreinadorModelo
from src.aplicacao.pokemon_schemas import InteracaoPokemonSchema
from src.aplicacao.casos_de_uso.gerenciar_pokemon import GerenciarPokemonCasoDeUso
from src.aplicacao.pokemon_schemas import InteracaoPokemonSchema, ListaMovimentosSchema

router = APIRouter(prefix="/api/v1", tags=["Pokémon"])

@router.post("/favoritar", status_code=status.HTTP_200_OK)
def favoritar_pokemon(
    dados: InteracaoPokemonSchema,
    db: Session = Depends(obter_bd),
    treinador_atual: TreinadorModelo = Depends(obter_treinador_atual)
):
    caso_de_uso = GerenciarPokemonCasoDeUso(db)
    mensagem = caso_de_uso.alternar_favorito(treinador_id=treinador_atual.id, pokemon_id=dados.pokemon_id)
    return {"mensagem": mensagem}

@router.post("/capturar", status_code=status.HTTP_201_CREATED)
def capturar_pokemon(
    dados: InteracaoPokemonSchema,
    db: Session = Depends(obter_bd),
    treinador_atual: TreinadorModelo = Depends(obter_treinador_atual)
):
    caso_de_uso = GerenciarPokemonCasoDeUso(db)
    mensagem = caso_de_uso.capturar_pokemon(treinador_id=treinador_atual.id, pokemon_id=dados.pokemon_id)
    return {"mensagem": mensagem}

@router.get("/pokemon/{pokemon_id}/movimentos", response_model=ListaMovimentosSchema, status_code=status.HTTP_200_OK)
def listar_movimentos_pokemon(
    pokemon_id: int,
    db: Session = Depends(obter_bd),
    treinador_atual: TreinadorModelo = Depends(obter_treinador_atual) # Exige login
):
    caso_de_uso = GerenciarPokemonCasoDeUso(db)
    return caso_de_uso.listar_movimentos(pokemon_id)