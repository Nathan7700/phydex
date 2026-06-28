# src/infrastructure/database/repositories/poke_db_repository.py
from sqlalchemy.orm import Session, joinedload
from typing import List
from src.domain.repositories.ipoke_repository import IPokeRepository
from src.infrastructure.database.models.poke_model import PokemonModel
from src.infrastructure.database.models.type_model import TypeModel
from src.infrastructure.database.models.pokemon_type_model import PokemonTypeModel
from src.infrastructure.database.models.game_model import GameModel

class PokeDbRepository(IPokeRepository):
    def __init__(self, db: Session):
        self.db = db

    def pokemon_exists(self, pokedex_number: int) -> bool:
        return self.db.query(PokemonModel).filter(PokemonModel.pokedex_number == pokedex_number).first() is not None

    def save_type_if_not_exists(self, name: str) -> int:
        pokemon_type = self.db.query(TypeModel).filter(TypeModel.name == name).first()
        if not pokemon_type:
            pokemon_type = TypeModel(name=name)
            self.db.add(pokemon_type)
            self.db.commit()
            self.db.refresh(pokemon_type)
        return pokemon_type.id

    def save_pokemon(self, pokemon_data: dict, type_ids: list[int]) -> None:
        new_pokemon = PokemonModel(**pokemon_data)
        self.db.add(new_pokemon)
        self.db.commit()
        self.db.refresh(new_pokemon)

        # Insere os registros na tabela associativa respeitando os slots (RN7)
        for index, type_id in enumerate(type_ids):
            association = PokemonTypeModel(
                pokemon_id=new_pokemon.id,
                type_id=type_id,
                slot=index + 1  # Slot 1 = Primário, Slot 2 = Secundário
            )
            self.db.add(association)
        
        self.db.commit()
        

    def get_paginated_list(self, limit: int, offset: int) -> List[PokemonModel]:
        return (
            self.db.query(PokemonModel)
            .options(joinedload(PokemonModel.types)) # Carrega os tipos na mesma query
            .order_by(PokemonModel.pokedex_number.asc())
            .offset(offset)
            .limit(limit)
            .all()
        )
    
    def save_game_if_not_exists(self, game_name: str, generation: int, region: str):
            game_name_lower = game_name.lower().strip()
            exist = self.db.query(GameModel).filter(GameModel.name == game_name_lower).first()
            
            if not exist:
                # Enviamos os campos obrigatórios exigidos pelo banco de dados
                novo_jogo = GameModel(
                    name=game_name_lower,
                    generation=generation,
                    region=region.capitalize()
                )
                self.db.add(novo_jogo)
                self.db.commit()