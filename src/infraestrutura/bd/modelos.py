from sqlalchemy import Column, Integer, String, ForeignKey
from src.infraestrutura.bd.sessao import Base

class TreinadorModelo(Base):
    __tablename__ = "treinadores"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    senha_hash = Column(String, nullable=False)

class FavoritoModelo(Base):
    __tablename__ = "treinador_favoritos"

    treinador_id = Column(Integer, ForeignKey("treinadores.id", ondelete="CASCADE"), primary_key=True)
    pokemon_id = Column(Integer, primary_key=True)

class CapturadoModelo(Base):
    __tablename__ = "treinador_capturados"

    treinador_id = Column(Integer, ForeignKey("treinadores.id", ondelete="CASCADE"), primary_key=True)
    pokemon_id = Column(Integer, primary_key=True)

class MovimentoModelo(Base):
    __tablename__ = "movimentos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, nullable=False)
    tipo = Column(String, nullable=False)
    poder = Column(Integer, nullable=True)
    pp = Column(Integer, nullable=False)