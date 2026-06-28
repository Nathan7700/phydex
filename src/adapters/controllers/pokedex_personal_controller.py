from sqlalchemy.orm import Session
from src.infrastructure.services.pokeapi_client import PokeApiClient
from src.usecases.pokedex_personal.fav_poke_usecase import FavoritePokemonUseCase
from src.usecases.pokedex_personal.capture_poke_usecase import CapturePokemonUseCase


class PokedexPersonalController:
    def __init__(self, db: Session):
        self.db = db
        self.api_client = PokeApiClient()


    def favoritar(self, user_id: int, pokemon_id: int):
        # Primeiro, valida na PokéAPI externa se o Pokémon existe de verdade
        nome_pokemon = self.api_client.buscar_nome_por_id(pokemon_id)
       
        # Se não levantou erro, executa o caso de uso de persistência
        use_case = FavoritePokemonUseCase(self.db)
        resultado = use_case.executar(user_id, pokemon_id)
        resultado["pokemon_nome"] = nome_pokemon
        return resultado


    def capturar(self, user_id: int, pokemon_id: int):
        nome_pokemon = self.api_client.buscar_nome_por_id(pokemon_id)
       
        use_case = CapturePokemonUseCase(self.db)
        resultado = use_case.executar(user_id, pokemon_id)
        resultado["pokemon_nome"] = nome_pokemon
        return resultado
