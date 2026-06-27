from sqlalchemy.orm import Session

class PokedexPersonalController:
    def __init__(self, db: Session):
        self.db = db

    def favoritar_pokemon(self, user_id: int, pokemon_id: int) -> dict:
        return {"mensagem": "Pokémon favoritado com sucesso!"}

    def capturar_pokemon(self, user_id: int, pokemon_id: int) -> dict:
        return {"mensagem": "Pokémon capturado com sucesso!"}