from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR

from src.infrastructure.api.routes.auth_routes import router as auth_router
from src.infrastructure.api.routes.pokedex_routes import router as pokedex_personal_router
from src.infrastructure.api.routes.team_routes import router as team_router
from src.infrastructure.api.routes.poke_routes import router as pokemon_general_router

app = FastAPI(title="PhyDex API", version="1.0.0")

# # MIDDLEWARE GLOBAL / EXCEPTION HANDLERS
@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(status_code=HTTP_400_BAD_REQUEST, content={"error": "Bad Request", "message": str(exc)})

@app.exception_handler(KeyError)
async def key_error_handler(request: Request, exc: KeyError):
    return JSONResponse(status_code=HTTP_404_NOT_FOUND, content={"error": "Not Found", "message": str(exc).strip("'")})

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=HTTP_500_INTERNAL_SERVER_ERROR, content={"error": "Internal Server Error", "message": "Erro interno."})

# ROTAS CONFIGURADAS
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(pokemon_general_router, prefix="/api/v1/pokemons", tags=["Pokédex Core"])
app.include_router(pokedex_personal_router, prefix="/api/v1/pokedex", tags=["Personal Pokédex"])
app.include_router(team_router, prefix="/api/v1/teams", tags=["Team Builder"])

@app.get("/")
def read_root(): 
    return {"message": "API Online"}