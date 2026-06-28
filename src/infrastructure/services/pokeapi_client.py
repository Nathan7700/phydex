# src/infrastructure/services/pokeapi_client.py
import requests
from src.domain.services.ipokedex_service import IPokedexService

class PokeApiClient(IPokedexService):
    """Responsável exclusivo por se comunicar com a API externa PokéAPI."""

    def __init__(self):
        self.base_url = "https://pokeapi.co/api/v2"

    # O nome aqui deve bater EXATAMENTE com o método abstrato que deu erro no terminal
    def buscar_dados_externos_pokemon(self, pokemon_id: int) -> dict:
        url = f"{self.base_url}/pokemon/{pokemon_id}"
        
        try:
            resposta = requests.get(url)
            
            if resposta.status_code == 404:
                raise ValueError("Pokémon não encontrado na PokéAPI externa.")
                
            resposta.raise_for_status()
            return resposta.json()  # Retorna o dicionário completo com os dados do Pokémon
            
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Erro de conexão com a PokéAPI: {str(e)}")