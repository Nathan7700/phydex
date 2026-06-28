from sqlalchemy.orm import Session
from src.infrastructure.database.models import FavModel


class FavoritePokemonUseCase:
    """Regra de negócio para o Usuário favoritar um Pokémon."""
   
    def __init__(self, db: Session):
        self.db = db


    def executar(self, user_id: int, pokemon_id: int) -> dict:
        # Verifica se já está favoritado
        already_fav = self.db.query(FavModel).filter(
            FavModel.user_id == user_id,
            FavModel.pokemon_id == pokemon_id
        ).first()


        if already_fav:
            return {"mensagem": "Pokémon já está nos favoritos."}


        new_fav = FavModel(user_id=user_id, pokemon_id=pokemon_id)
        self.db.add(new_fav)
        self.db.commit()
       
        return {"mensagem": "Pokémon favoritado com sucesso!"}
