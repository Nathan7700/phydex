from typing import List
from uuid import UUID, uuid4

class Team:
    def __init__(self, trainer_id: UUID, name: str, pokemon_ids: List[int] = None, id: UUID = None):
        self.id = id or uuid4()
        self.trainer_id = trainer_id
        self.name = name
        self.pokemon_ids = pokemon_ids or []
        self.validate()

    def validate(self):
        if len(self.pokemon_ids) > 6:
            raise ValueError("Uma equipe não pode ter mais de 6 Pokémon.")