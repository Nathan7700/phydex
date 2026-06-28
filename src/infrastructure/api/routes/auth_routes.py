from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.infrastructure.database.config import get_db

# Importa o schema e o caso de uso das novas pastas em inglês
from src.adapters.schemas.auth_schemas import TrainerLoginSchema, TokenSchema
from src.usecases.auth.autenticate_trainer_usecase import AuthenticateTrainerUseCase

router = APIRouter()

@router.post("/login", response_model=TokenSchema)
def login(payload: TrainerLoginSchema, db: Session = Depends(get_db)):
    try:
        # Invoca o caso de uso que realocamos anteriormente
        use_case = AuthenticateTrainerUseCase(db)
        return use_case.executar(payload)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )