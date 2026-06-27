from sqlalchemy.orm import Session
from src.infrastructure.db.models import CapturadoModelo

class CapturePokemonUseCase:
    """Regra de negócio para o Usuário marcar um Pokémon como capturado."""
    
    def __init__(self, db: Session):
        self.db = db

    def executar(self, user_id: int, pokemon_id: int) -> dict:
        ja_capturado = self.db.query(CapturadoModelo).filter(
            CapturadoModelo.user_id == user_id,
            CapturadoModelo.pokemon_id == pokemon_id
        ).first()

        if ja_capturado:
            return {"mensagem": "Pokémon já foi marcado como capturado anteriormente."}

        novo_capturado = CapturadoModelo(user_id=user_id, pokemon_id=pokemon_id)
        self.db.add(novo_capturado)
        self.db.commit()
        
        return {"mensagem": "Pokémon adicionado à sua Pokédex pessoal!"}