from fastapi import FastAPI
from src.infraestrutura.bd.sessao import engine
from src.infraestrutura.bd.modelos import Base
from src.apresentacao.rotas_auth import router as auth_router
from src.apresentacao.rotas_pokemon import router as pokemon_router

# Cria as tabelas no banco de dados (phydex.db) se elas não existirem
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Phydex API", version="1.0.0")

# Registra as rotas de autenticação no app principal
app.include_router(auth_router)
app.include_router(pokemon_router)

@app.get("/")
def raiz():
    return {"mensagem": "Bem-vindo à API Phydex!"}