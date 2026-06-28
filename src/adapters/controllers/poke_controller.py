# src/adapters/controllers/poke_controller.py
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import List
from infrastructure.database.session import obter_sessao # Troque pelo nome exato da sua função de sessão
from src.infrastructure.database.repositories.poke_db_repository import PokeDbRepository
from src.usecases.pokemon.list_pokedex_usecase import ListPokedexUseCase
from src.adapters.schemas.pokedex_schemas import PokemonBoxResponseSchema

router = APIRouter(prefix="/v1/pokemons", tags=["Pokédex Core"])

@router.get("", response_model=List[PokemonBoxResponseSchema], status_code=status.HTTP_200_OK)
def get_base_pokedex(
    page: int = Query(default=1, ge=1, description="Número da página atual"),
    per_page: int = Query(default=20, ge=1, le=100, description="Quantidade de itens por página"),
    db: Session = Depends(obter_sessao)
):
    """
    Retorna a listagem base de Pokémon paginada em formato de caixas (cards) para a Home.
    """
    # Inversão de dependência acontecendo de forma limpa na camada de entrega
    poke_repository = PokeDbRepository(db)
    use_case = ListPokedexUseCase(poke_repository)
    
    # Executa a regra de negócio
    pokemons_list = use_case.execute(page=page, per_page=per_page)
    
    return pokemons_list