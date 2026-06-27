from pydantic import BaseModel, EmailStr, Field

class TrainerRegisterSchema(BaseModel):
    """Validates data sent when a new App User (Trainer) registers."""
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)

class TrainerLoginSchema(BaseModel):
    """Validates credentials sent during App login."""
    email: EmailStr
    password: str

class TokenSchema(BaseModel):
    """Validates the standard format of the returned JWT Access Token."""
    access_token: str
    token_type: str