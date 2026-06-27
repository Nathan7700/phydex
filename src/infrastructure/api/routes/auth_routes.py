from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

def get_db(): return None  # Isolado para evitar erro do psycopg2

from src.adapters.schemas.auth_schemas import TrainerLoginSchema, TokenSchema
from src.usecases.auth.autenticate_trainer_usecase import AuthenticateTrainerUseCase

router = APIRouter()

@router.post("/login", response_model=TokenSchema)
def login(payload: TrainerLoginSchema, db: Session = Depends(get_db)):
    use_case = AuthenticateTrainerUseCase(db)
    return use_case.executar(payload)