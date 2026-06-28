from sqlalchemy.orm import Session
from src.domain.repositories.itrainer_repository import ITrainerRepository
from src.infrastructure.database.models.trainer_model import TrainerModel

class TrainerRepository(ITrainerRepository):
    
    def __init__(self, db: Session):
        self.db = db  # A sessão do banco fica isolada dentro do adaptador concreto

    def get_by_email(self, email: str):
        return self.db.query(TrainerModel).filter(TrainerModel.email == email).first()

    def create(self, trainer_data: dict):
        db_trainer = TrainerModel(
            username=trainer_data["username"],
            email=trainer_data["email"],
            password_hash=trainer_data["password_hash"]
        )
        self.db.add(db_trainer)
        self.db.commit()
        self.db.refresh(db_trainer)
        return db_trainer