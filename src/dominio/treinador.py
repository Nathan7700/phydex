from dataclasses import dataclass
from typing import Optional

@dataclass
class Treinador:
    id: Optional[int]
    nome: str
    email: str
    senha_hash: str