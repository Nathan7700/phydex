# src/infrastructure/database/models/poke_model.py
from sqlalchemy import Column, Integer, String, SmallInteger, Text, Numeric
from sqlalchemy.orm import relationship
from src.infrastructure.database.session import Base

class PokemonModel(Base):
    """Mapeia rigidamente a tabela 'pokemon' do DER oficial."""
    __tablename__ = "pokemon"

    id = Column(Integer, primary_key=True, autoincrement=True)  # SERIAL PK [cite: 294]
    pokedex_number = Column(Integer, nullable=False)            # INTEGER [cite: 294]
    name = Column(String(100), nullable=False)                  # VARCHAR(100) [cite: 294]
    species = Column(String(100), nullable=False)               # VARCHAR(100) [cite: 294]
    description = Column(Text, nullable=False)                  # TEXT [cite: 294]
    image_url = Column(Text, nullable=False)                    # TEXT [cite: 294]
    
    # Atributos Físicos (Corrigido de Decimal para Numeric para o SQLAlchemy)
    height = Column(Numeric(5, 2), nullable=False)              # DECIMAL(5,2) [cite: 296]
    weight = Column(Numeric(6, 2), nullable=False)              # DECIMAL(6,2) [cite: 296]
    
    # Stats Base (SMALLINT mapeado via SmallInteger para economia no Supabase)
    base_hp = Column(SmallInteger, nullable=False)              # SMALLINT [cite: 296]
    base_attack = Column(SmallInteger, nullable=False)          # SMALLINT [cite: 296]
    base_defense = Column(SmallInteger, nullable=False)         # SMALLINT [cite: 296]
    base_sp_attack = Column(SmallInteger, nullable=False)       # SMALLINT [cite: 296]
    base_sp_defense = Column(SmallInteger, nullable=False)      # SMALLINT [cite: 296]
    base_speed = Column(SmallInteger, nullable=False)           # SMALLINT [cite: 296]
    
    # Dados de Experiência e Evolução
    base_exp = Column(SmallInteger, nullable=False)             # SMALLINT [cite: 296]
    base_friendship = Column(SmallInteger, nullable=False)      # SMALLINT [cite: 296]
    growth_rate = Column(String(50), nullable=False)            # VARCHAR(50) [cite: 296]
    
    # Gênero e Dados de Breeding (Suporta: MaleOnly, FemaleOnly, MaleFemale, Genderless)
    gender_type = Column(String(20), nullable=False)            # VARCHAR(20) [cite: 296, 297]
    male_percentage = Column(Numeric(5, 2), nullable=True)      # DECIMAL(5,2) NULL [cite: 296]
    female_percentage = Column(Numeric(5, 2), nullable=True)    # DECIMAL(5,2) NULL [cite: 296]
    egg_cycles = Column(SmallInteger, nullable=False)           # SMALLINT [cite: 296]

    # Relacionamento carregado dinamicamente através da tabela associativa pokemon_type
    types = relationship("TypeModel", secondary="pokemon_type", backref="pokemons")