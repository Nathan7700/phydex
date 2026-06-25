from pydantic import BaseModel

class InteracaoPokemonSchema(BaseModel):
    pokemon_id: int

    class Config:
        from_attributes = True

from pydantic import BaseModel
from typing import List, Optional

# ... (Mantenha o InteracaoPokemonSchema que já existe aí)

class MovimentoDetalheSchema(BaseModel):
    nome: str
    tipo: str
    poder: Optional[int] = None
    precisao: Optional[int] = None

class ListaMovimentosSchema(BaseModel):
    pokemon_id: int
    pokemon_nome: str
    movimentos: List[MovimentoDetalheSchema]