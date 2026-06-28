from sqlalchemy import Column, Integer, String, SmallInteger
from src.infrastructure.database.session import Base

class GameModel(Base):
    """Mapeia rigidamente a tabela 'game' do DER oficial"""
    __tablename__ = "game"

    id = Column(Integer, primary_key=True, autoincrement=True)  # SERIAL PK
    name = Column(String(100), nullable=False)                 # VARCHAR(100)
    generation = Column(SmallInteger, nullable=False)          # SMALLINT
    region = Column(String(50), nullable=False)                # VARCHAR(50)