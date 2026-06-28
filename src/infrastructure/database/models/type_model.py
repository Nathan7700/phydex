# src/infrastructure/database/models/type_model.py
from sqlalchemy import Column, String, SmallInteger
from src.infrastructure.database.session import Base

class TypeModel(Base):
    """Mapeia rigidamente a tabela 'type' do DER oficial"""
    __tablename__ = "type"

    id = Column(SmallInteger, primary_key=True, autoincrement=True)  # SMALLSERIAL PK
    name = Column(String(30), unique=True, nullable=False)          # VARCHAR(30)