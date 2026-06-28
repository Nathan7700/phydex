# src/domain/repositories/ipoke_repository.py
from abc import ABC, abstractmethod
from typing import List, Any

class IPokeRepository(ABC):
    
    @abstractmethod
    def pokemon_exists(self, pokedex_number: int) -> bool:
        """Checks if a Pokémon species already exists in the database."""
        pass

    @abstractmethod
    def save_type_if_not_exists(self, name: str) -> int:
        """Saves a type elemental name and returns its database ID."""
        pass

    @abstractmethod
    def save_pokemon(self, pokemon_data: dict, type_ids: list[int]) -> None:
        """Persists the complete Pokémon data and links its elemental types."""
        pass

    @abstractmethod
    def get_paginated_list(self, limit: int, offset: int) -> List[Any]:
        """Busca uma lista paginada de Pokémon incluindo seus tipos elementais."""
        pass