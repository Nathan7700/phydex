from uuid import UUID
from src.usecases.team_builder.manage_team_usecase import ManageTeamUseCase
from src.adapters.schemas.team_schemas import TeamCreateSchema

class TeamController:
    def __init__(self, manage_team_usecase: ManageTeamUseCase):
        self.usecase = manage_team_usecase

    def create(self, trainer_id: UUID, data: TeamCreateSchema):
        return self.usecase.create_team(trainer_id, data.name, data.pokemon_ids)

    def get(self, team_id: UUID):
        return self.usecase.get_team(team_id)

    def get_all_from_trainer(self, trainer_id: UUID):
        return self.usecase.get_trainer_teams(trainer_id)

    def update(self, team_id: UUID, data: TeamCreateSchema):
        return self.usecase.update_team(team_id, data.name, data.pokemon_ids)

    def delete(self, team_id: UUID):
        self.usecase.delete_team(team_id)
        return {"message": "Equipe deletada com sucesso."}