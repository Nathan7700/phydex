# populate.py
from src.infrastructure.database.session import SessionLocal, engine
from src.infrastructure.database.models import Base
from src.infrastructure.database.repositories.poke_db_repository import PokeDbRepository
from src.infrastructure.services.pokeapi_client import PokeApiClient
from src.usecases.pokemon.populate_pokedex_usecase import PopulatePokedexUseCase

def run_population():
    print("Criando tabelas no banco de dados caso não existam...")
    Base.metadata.create_all(bind=engine)
    
    db_session = SessionLocal()
    repository = PokeDbRepository(db_session)
    api_client = PokeApiClient()
    
    # 1. Garantindo a presença de todos os 18 tipos elementais
    print("Garantindo a presença de todos os 18 tipos elementais oficiais...")
    official_types = [
        "normal", "fire", "water", "grass", "electric", "ice",
        "fighting", "poison", "ground", "flying", "psychic", "bug",
        "rock", "ghost", "dragon", "steel", "dark", "fairy"
    ]
    for type_name in official_types:
        repository.save_type_if_not_exists(type_name)

    # 2. CORREÇÃO: Garantindo a presença dos jogos principais com dados completos
    print("Garantindo a presença dos jogos no banco...")
    official_games = [
        {"name": "red", "generation": 1, "region": "kanto"},
        {"name": "blue", "generation": 1, "region": "kanto"},
        {"name": "yellow", "generation": 1, "region": "kanto"},
        {"name": "firered", "generation": 1, "region": "kanto"},
        {"name": "leafgreen", "generation": 1, "region": "kanto"},
        {"name": "gold", "generation": 2, "region": "johto"},
        {"name": "silver", "generation": 2, "region": "johto"},
        {"name": "crystal", "generation": 2, "region": "johto"},
        {"name": "heartgold", "generation": 2, "region": "johto"},
        {"name": "soulsilver", "generation": 2, "region": "johto"},
        {"name": "ruby", "generation": 3, "region": "hoenn"},
        {"name": "sapphire", "generation": 3, "region": "hoenn"},
        {"name": "emerald", "generation": 3, "region": "hoenn"},
        {"name": "diamond", "generation": 4, "region": "sinnoh"},
        {"name": "pearl", "generation": 4, "region": "sinnoh"},
        {"name": "platinum", "generation": 4, "region": "sinnoh"}
    ]
    
    for game_data in official_games:
        repository.save_game_if_not_exists(
            game_name=game_data["name"],
            generation=game_data["generation"],
            region=game_data["region"]
        )
    
    # 3. Execução do Caso de Uso para os Pokémon
    use_case = PopulatePokedexUseCase(repository, api_client)
    
    print("Iniciando o loop de carga de dados para a 1ª Geração (IDs 1 a 151)...")
    use_case.execute(1, 151)
    print("População do banco de dados concluída com sucesso!")

if __name__ == "__main__":
    run_population()