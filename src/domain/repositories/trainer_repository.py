from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from src.domain.entities.team import Team

class TeamRepositoryInterface(ABC):
    @abstractmethod
    def save(self, team: Team) -> Team:
        pass

    @abstractmethod
    def get_by_id(self, team_id: UUID) -> Optional[Team]:
        pass

    @abstractmethod
    def get_by_trainer_id(self, trainer_id: UUID) -> List[Team]:
        pass

    @abstractmethod
    def update(self, team: Team) -> Team:
        pass

    @abstractmethod
    def delete(self, team_id: UUID) -> bool:
        pass