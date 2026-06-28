# src/usecases/pokemon/list_pokedex_usecase.py
from typing import List, Dict, Any
from src.domain.repositories.ipoke_repository import IPokeRepository

class ListPokedexUseCase:
    def __init__(self, poke_repo: IPokeRepository):
        self.poke_repo = poke_repo

    def execute(self, page: int, per_page: int) -> List[Dict[str, Any]]:
        if page < 1:
            page = 1
        if per_page < 1 or per_page > 100: # Proteção contra paginações abusivas
            per_page = 20

        # Cálculo matemático do offset para o banco de dados
        offset = (page - 1) * per_page

        pokemons = self.poke_repo.get_paginated_list(limit=per_page, offset=offset)

        # Formata a estrutura de dicionário puro de domínio (View Model simplificado para as caixas)
        results = []
        for p in pokemons:
            # Ordena os tipos pelo slot (Primário primeiro, Secundário depois - RN7)
            sorted_types = sorted(p.types, key=lambda t: t.id) # Se houver o slot mapeado na associação, use-o
            
            results.append({
                "id": p.id,
                "pokedex_number": p.pokedex_number,
                "name": p.name,
                "image_url": p.image_url,
                "types": [t.name.capitalize() for t in p.types] # Retorna a lista de strings dos tipos
            })

        return results