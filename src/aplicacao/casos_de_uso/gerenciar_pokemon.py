import requests
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.infraestrutura.bd.modelos import FavoritoModelo, CapturadoModelo

class GerenciarPokemonCasoDeUso:
    def __init__(self, db: Session):
        self.db = db

    def _buscar_nome_pokemon(self, pokemon_id: int) -> str:
        """Busca o nome do Pokémon na PokeAPI usando o ID"""
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
        try:
            resposta = requests.get(url, timeout=5)
            if resposta.status_code == 404:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, 
                    detail=f"Pokémon com ID {pokemon_id} não existe na PokeAPI!"
                )
            dados = resposta.json()
            return dados["name"].capitalize()  # Deixa a primeira letra maiúscula (ex: Bulbasaur)
        except requests.RequestException:
            # Caso a PokeAPI esteja fora do ar, usa um nome genérico para não travar o sistema
            return f"Pokémon #{pokemon_id}"

    def alternar_favorito(self, treinador_id: int, pokemon_id: int) -> str:
        # Busca o nome real antes de qualquer ação
        nome_pokemon = self._buscar_nome_pokemon(pokemon_id)

        favorito = self.db.query(FavoritoModelo).filter_by(
            treinador_id=treinador_id, pokemon_id=pokemon_id
        ).first()

        if favorito:
            self.db.delete(favorito)
            self.db.commit()
            return f"{nome_pokemon} foi removido dos seus favoritos!"
        else:
            novo_favorito = FavoritoModelo(treinador_id=treinador_id, pokemon_id=pokemon_id)
            self.db.add(novo_favorito)
            self.db.commit()
            return f"{nome_pokemon} foi adicionado aos seus favoritos com sucesso!"

    def capturar_pokemon(self, treinador_id: int, pokemon_id: int) -> str:
        nome_pokemon = self._buscar_nome_pokemon(pokemon_id)

        capturado = self.db.query(CapturadoModelo).filter_by(
            treinador_id=treinador_id, pokemon_id=pokemon_id
        ).first()

        if capturado:
            return f"Você já capturou esse {nome_pokemon}!"
        
        novo_capturado = CapturadoModelo(treinador_id=treinador_id, pokemon_id=pokemon_id)
        self.db.add(novo_capturado)
        self.db.commit()
        return f"{nome_pokemon} capturado com sucesso e guardado na pokebola!"

    def listar_movimentos(self, pokemon_id: int) -> dict:
        """Busca os movimentos de um Pokémon na PokeAPI e formata os dados"""
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
        try:
            resposta = requests.get(url, timeout=5)
            if resposta.status_code == 404:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, 
                    detail=f"Pokémon com ID {pokemon_id} não existe!"
                )
            
            dados_pokemon = resposta.json()
            nome_pokemon = dados_pokemon["name"].capitalize()
            
            movimentos_formatados = []
            
            # Vamos pegar apenas os 10 primeiros movimentos para a resposta não ficar gigante e lenta
            para_buscar = dados_pokemon["moves"][:10]
            
            for item in para_buscar:
                move_url = item["move"]["url"]
                res_move = requests.get(move_url, timeout=3)
                
                if res_move.status_code == 200:
                    dados_move = res_move.json()
                    movimentos_formatados.append({
                        "nome": dados_move["name"].replace("-", " ").capitalize(),
                        "tipo": dados_move["type"]["name"].capitalize(),
                        "poder": dados_move.get("power"),
                        "precisao": dados_move.get("accuracy")
                    })
            
            return {
                "pokemon_id": pokemon_id,
                "pokemon_nome": nome_pokemon,
                "movimentos": movimentos_formatados
            }
            
        except requests.RequestException:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Erro ao conectar com a PokeAPI."
            )