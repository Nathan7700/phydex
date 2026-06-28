from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
# Importa a Base configurada no seu arquivo database/config.py
from src.infrastructure.database.config import Base

class TrainerModel(Base):
    __tablename__ = "trainers"

    # Chave primária da tabela física
    id = Column(Integer, primary_key=True, index=True)
   
    # Campos básicos do Treinador (ajuste de acordo com o seu domínio)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)


    # Exemplo de relacionamentos futuros (opcional, baseado na sua estrutura):
    # Se um treinador tem favoritos ou pokémons capturados, mapeia-se aqui.
    # favorites = relationship("FavoriteModel", back_populates="trainer")
    # captured = relationship("CapturedModel", back_populates="trainer")
