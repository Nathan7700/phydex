from pydantic import BaseModel, Field
from typing import List
from uuid import UUID

class TeamCreateSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    pokemon_ids: List[int] = Field(..., description="Lista de IDs dos Pokémon")

class TeamResponseSchema(BaseModel):
    id: UUID
    trainer_id: UUID
    name: str
    pokemon_ids: List[int]

    class Config:
        from_attributes = True