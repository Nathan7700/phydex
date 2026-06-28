from pydantic import BaseModel
from typing import List

class PokemonBoxResponseSchema(BaseModel):
    id: int
    pokedex_number: int
    name: str
    image_url: str
    types: List[str]

    class Config:
        from_attributes = True