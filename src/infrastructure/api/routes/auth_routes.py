from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.infrastructure.db.config import get_db

# Importa o schema e o caso de uso das novas pastas em inglês
from src.adapters.schemas.auth_schemas import TrainerLoginSchema, TokenSchema
from src.usecases.auth.login_user_usecase import LoginUserUseCase

router = APIRouter()

@router.post("/login", response_model=TokenSchema)
def login(payload: TrainerLoginSchema, db: Session = Depends(get_db)):
    try:
        # Invoca o caso de uso que realocamos anteriormente
        use_case = LoginUserUseCase(db)
        return use_case.executar(payload)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )