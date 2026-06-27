from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.infrastructure.db.config import get_db

# Importa o middleware de segurança e o controlador em inglês
from src.infrastructure.auth.jwt_middleware import get_current_user
from src.infrastructure.db.models.trainer_model import TrainerModel
from src.adapters.schemas.pokedex_schemas import PokemonInteractionSchema
from src.adapters.controllers.pokedex_personal_controller import PokedexPersonalController

router = APIRouter()

@router.post("/favorite", status_code=status.HTTP_200_OK)
def favorite_pokemon(
    payload: PokemonInteractionSchema, 
    db: Session = Depends(get_db),
    current_user: TrainerModel = Depends(get_current_user)
):
    # O controlador orquestra a validação na PokéAPI e a persistência no banco
    controller = PokedexPersonalController(db)
    return controller.favoritar_pokemon(user_id=current_user.id, pokemon_id=payload.pokemon_id)

@router.post("/capture", status_code=status.HTTP_200_OK)
def capture_pokemon(
    payload: PokemonInteractionSchema, 
    db: Session = Depends(get_db),
    current_user: TrainerModel = Depends(get_current_user)
):
    controller = PokedexPersonalController(db)
    return controller.capturar_pokemon(user_id=current_user.id, pokemon_id=payload.pokemon_id)