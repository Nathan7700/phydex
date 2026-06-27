import requests
from fastapi import HTTPException, status

class PokeApiClient:
    """Responsável exclusivo por se comunicar com a API externa PokéAPI."""
    
    def __init__(self):
        self.base_url = "https://pokeapi.co/api/v2/pokemon"

    def buscar_nome_por_id(self, pokemon_id: int) -> str:
        try:
            url = f"{self.base_url}/{pokemon_id}"
            resposta = requests.get(url)
            
            if resposta.status_code == 404:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, 
                    detail="Pokémon não encontrado na PokéAPI externa."
                )
            
            dados = resposta.json()
            return dados["name"]
        except requests.exceptions.RequestException as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Erro de conexão com a PokéAPI: {str(e)}"
            )