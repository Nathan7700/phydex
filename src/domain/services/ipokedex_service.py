from abc import ABC, abstractmethod

class IPokedexService(ABC):
    @abstractmethod
    def buscar_dados_externos_pokemon(self, pokemon_id: int) -> dict:
        pass