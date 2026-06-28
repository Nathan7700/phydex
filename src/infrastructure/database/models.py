from sqlalchemy import Column, Integer, String, ForeignKey
from infrastructure.database.session import Base

class TrainerModel(Base):
    __tablename__ = "trainer"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)

class FavModel(Base):
    __tablename__ = "trainer_favs"

    trainer_id = Column(Integer, ForeignKey("trainer.id", ondelete="CASCADE"), primary_key=True)
    pokemon_id = Column(Integer, primary_key=True)

class CapturedModel(Base):
    __tablename__ = "trainer_captured"

    trainer_id = Column(Integer, ForeignKey("trainer.id", ondelete="CASCADE"), primary_key=True)
    pokemon_id = Column(Integer, primary_key=True)

class MoveModel(Base):
    __tablename__ = "move"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    type = Column(String, nullable=False)
    power = Column(Integer, nullable=True)
    pp = Column(Integer, nullable=False)