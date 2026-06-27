from dataclasses import dataclass
from typing import Optional

@dataclass
class Trainer:
    """Conceptual model representing the App User (the Trainer who logs in)."""
    id: Optional[int]
    name: str
    email: str
    password_hash: str