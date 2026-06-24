from pydantic import BaseModel, EmailStr, Field

class TreinadorCadastroSchema(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    senha: str = Field(..., min_length=6)

class TreinadorLoginSchema(BaseModel):
    email: EmailStr
    senha: str

class TokenSchema(BaseModel):
    access_token: str
    token_type: str