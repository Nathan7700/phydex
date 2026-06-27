from typing import List, Optional
from uuid import UUID
from src.domain.entities.team import Team

class ManageTeamUseCase:
    def __init__(self, team_repository):
        self.team_repository = team_repository

    def create_team(self, trainer_id: UUID, name: str, pokemon_ids: List[int]) -> Team:
        new_team = Team(trainer_id=trainer_id, name=name, pokemon_ids=pokemon_ids)
        return self.team_repository.save(new_team)

    def get_team(self, team_id: UUID) -> Optional[Team]:
        team = self.team_repository.get_by_id(team_id)
        if not team:
            raise KeyError("Equipe não encontrada.")
        return team

    def get_trainer_teams(self, trainer_id: UUID) -> List[Team]:
        return self.team_repository.get_by_trainer_id(trainer_id)

    def update_team(self, team_id: UUID, name: str, pokemon_ids: List[int]) -> Team:
        team = self.get_team(team_id)
        team.name = name
        team.pokemon_ids = pokemon_ids
        team.validate()
        return self.team_repository.update(team)

    def delete_team(self, team_id: UUID) -> bool:
        self.get_team(team_id)
        return self.team_repository.delete(team_id)