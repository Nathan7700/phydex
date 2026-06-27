from fastapi import FastAPI
# Importa as rotas das novas localizações em inglês
from src.infrastructure.api.routes.auth_routes import router as auth_router
from src.infrastructure.api.routes.pokedex_routes import router as pokedex_router

app = FastAPI(title="PhyDex API", version="1.0.0")

# Inclui os roteadores com prefixos limpos e organizados
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(pokedex_router, prefix="/pokedex", tags=["Personal Pokedex"])

@app.get("/")
def read_root():
    return {"message": "Welcome to PhyDex API - Clean Architecture setup complete!"}