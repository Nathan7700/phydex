# src/domain/repositories/itrainer_repository.py
from abc import ABC, abstractmethod
from typing import Optional, Any

class ITrainerRepository(ABC):

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Any]:
        """Busca um treinador pelo e-mail cadastrado"""
        pass

    @abstractmethod
    def create(self, trainer_data: dict) -> Any:
        """Persiste um novo treinador no sistema"""
        pass