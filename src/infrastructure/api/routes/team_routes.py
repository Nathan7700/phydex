from fastapi import APIRouter, Depends, status
from uuid import UUID, uuid4
from typing import List
from src.adapters.controllers.team_controller import TeamController
from src.usecases.team_builder.manage_team_usecase import ManageTeamUseCase
from src.adapters.schemas.team_schemas import TeamCreateSchema, TeamResponseSchema
from src.domain.entities.team import Team

class InMemoryTeamRepository:
    def __init__(self): self.db = {}
    def save(self, team: Team): self.db[team.id] = team; return team
    def get_by_id(self, team_id: UUID): return self.db.get(team_id)
    def get_by_trainer_id(self, trainer_id: UUID): return [t for t in self.db.values() if t.trainer_id == trainer_id]
    def update(self, team: Team): self.db[team.id] = team; return team
    def delete(self, team_id: UUID): 
        if team_id in self.db: del self.db[team_id]; return True
        return False

repo_mock = InMemoryTeamRepository()
router = APIRouter()

def get_controller() -> TeamController:
    return TeamController(ManageTeamUseCase(repo_mock))

MOCK_TRAINER_ID = uuid4()

@router.post("/", response_model=TeamResponseSchema, status_code=status.HTTP_201_CREATED)
def create_team(data: TeamCreateSchema, controller: TeamController = Depends(get_controller)):
    return controller.create(MOCK_TRAINER_ID, data)

@router.get("/{team_id}", response_model=TeamResponseSchema)
def get_team(team_id: UUID, controller: TeamController = Depends(get_controller)):
    return controller.get(team_id)

@router.put("/{team_id}", response_model=TeamResponseSchema)
def update_team(team_id: UUID, data: TeamCreateSchema, controller: TeamController = Depends(get_controller)):
    return controller.update(team_id, data)

@router.delete("/{team_id}")
def delete_team(team_id: UUID, controller: TeamController = Depends(get_controller)):
    return controller.delete(team_id)