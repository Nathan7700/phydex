from sqlalchemy.orm import Session
from src.infrastructure.database.models import CapturedModel


class CapturePokemonUseCase:
    """Regra de negócio para o Usuário marcar um Pokémon como capturado."""
   
    def __init__(self, db: Session):
        self.db = db


    def executar(self, user_id: int, pokemon_id: int) -> dict:
        already_captured = self.db.query(CapturedModel).filter(
            CapturedModel.user_id == user_id,
            CapturedModel.pokemon_id == pokemon_id
        ).first()


        if already_captured:
            return {"mensagem": "Pokémon já foi marcado como capturado anteriormente."}


        new_capture = CapturedModel(user_id=user_id, pokemon_id=pokemon_id)
        self.db.add(new_capture)
        self.db.commit()
       
        return {"mensagem": "Pokémon adicionado à sua Pokédex pessoal!"}