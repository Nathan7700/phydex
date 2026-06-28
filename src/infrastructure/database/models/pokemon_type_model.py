# src/infrastructure/database/models/pokemon_type_model.py
from sqlalchemy import Column, Integer, ForeignKey, SmallInteger
from src.infrastructure.database.session import Base

class PokemonTypeModel(Base):
    """Mapeia a tabela associativa N:N 'pokemon_type' do DER oficial"""
    __tablename__ = "pokemon_type"

    pokemon_id = Column(Integer, ForeignKey("pokemon.id", ondelete="CASCADE"), primary_key=True)  # PK, FK
    type_id = Column(Integer, ForeignKey("type.id", ondelete="CASCADE"), primary_key=True)        # PK, FK
    slot = Column(SmallInteger, nullable=False)                                                  # SMALLINT