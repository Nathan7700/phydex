from pydantic import BaseModel
from typing import List, Optional

class MoveDetailSchema(BaseModel):
    name: str
    type: str
    power: Optional[int] = None
    accuracy: Optional[int] = None

class MoveListSchema(BaseModel):
    pokemon_id: int
    pokemon_name: str
    moves: List[MoveDetailSchema]