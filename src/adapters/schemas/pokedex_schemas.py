from pydantic import BaseModel

class PokemonInteractionSchema(BaseModel):
    pokemon_id: int

    class Config:
        from_attributes = True