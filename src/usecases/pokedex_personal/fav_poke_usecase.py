from sqlalchemy.orm import Session
from src.infrastructure.db.models import FavoritoModelo

class FavoritePokemonUseCase:
    """Regra de negócio para o Usuário favoritar um Pokémon."""
    
    def __init__(self, db: Session):
        self.db = db

    def executar(self, user_id: int, pokemon_id: int) -> dict:
        # Verifica se já está favoritado
        ja_favoritado = self.db.query(FavoritoModelo).filter(
            FavoritoModelo.user_id == user_id,
            FavoritoModelo.pokemon_id == pokemon_id
        ).first()

        if ja_favoritado:
            return {"mensagem": "Pokémon já está nos favoritos."}

        novo_favorito = FavoritoModelo(user_id=user_id, pokemon_id=pokemon_id)
        self.db.add(novo_favorito)
        self.db.commit()
        
        return {"mensagem": "Pokémon favoritado com sucesso!"}