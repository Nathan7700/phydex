# src/infrastructure/api/routes/pokedex_routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.infrastructure.database.config import get_db

router = APIRouter()

@router.get("")
def get_personal_pokedex(db: Session = Depends(get_db)):
    return {"message": "Sua Pokédex Pessoal"}