# src/infrastructure/api/routes/poke_routes.py
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import List

from infrastructure.database.session import obter_bd # Garanta que o nome bate com o seu sessao.py
from src.infrastructure.database.repositories.poke_db_repository import PokeDbRepository
from src.usecases.pokemon.list_pokedex_usecase import ListPokedexUseCase
from src.adapters.schemas.pokedex_schemas import PokemonBoxResponseSchema

# IMPORTANTE: Esse nome precisa ser exatamente 'router' para o main.py achar!
router = APIRouter()

@router.get("", response_model=List[PokemonBoxResponseSchema], status_code=status.HTTP_200_OK)
def get_base_pokedex(
    page: int = Query(default=1, ge=1, description="Numero da pagina atual"),
    per_page: int = Query(default=20, ge=1, le=100, description="Quantidade de itens por pagina"),
    db: Session = Depends(obter_bd)
):
    """
    Retorna a listagem base de Pokemon paginada para a Home.
    """
    poke_repository = PokeDbRepository(db)
    use_case = ListPokedexUseCase(poke_repository)
    
    pokemons_list = use_case.execute(page=page, per_page=per_page)
    
    return pokemons_list