from decimal import Decimal
import requests
from src.domain.repositories.ipoke_repository import IPokeRepository
from src.infrastructure.services.pokeapi_client import PokeApiClient

class PopulatePokedexUseCase:
    def __init__(self, poke_repo: IPokeRepository, api_client: PokeApiClient):
        self.poke_repo = poke_repo
        self.api_client = api_client

    def execute(self, start_id: int, end_id: int) -> None:
        for poke_id in range(start_id, end_id + 1):
            if self.poke_repo.pokemon_exists(poke_id):
                print(f"Pokémon ID {poke_id} já existe no banco de dados. Pulando...")
                continue
                
            try:
                # 1. Consome os dados brutos gerais e de espécie da PokéAPI
                base_url = f"https://pokeapi.co/api/v2/pokemon/{poke_id}"
                raw_response = requests.get(base_url).json()
                
                species_url = f"https://pokeapi.co/api/v2/pokemon-species/{poke_id}"
                species_response = requests.get(species_url).json()

                print(f"Processando e populando: {raw_response['name'].capitalize()}...")

                # 2. Processa e resolve as IDs dos tipos elementais (RN7)
                type_ids = []
                for t in raw_response["types"]:
                    type_name = t["type"]["name"]
                    resolved_id = self.poke_repo.save_type_if_not_exists(type_name)
                    type_ids.append(resolved_id)

                # 3. Filtra descrições e classificações textuais em inglês para o banco
                description = "No description available."
                for entry in species_response["flavor_text_entries"]:
                    if entry["language"]["name"] == "en":
                        description = entry["flavor_text"].replace("\n", " ").replace("\f", " ")
                        break

                species_genus = "Unknown"
                for genus in species_response["genera"]:
                    if genus["language"]["name"] == "en":
                        species_genus = genus["genus"]
                        break

                # 4. Traduz os inteiros de "gender_rate" da PokéAPI para as categorias do DER
                gender_rate = species_response["gender_rate"]
                if gender_rate == -1:
                    gender_type, male_pct, female_pct = "Genderless", None, None
                elif gender_rate == 8:
                    gender_type, male_pct, female_pct = "FemaleOnly", Decimal("0.00"), Decimal("100.00")
                elif gender_rate == 0:
                    gender_type, male_pct, female_pct = "MaleOnly", Decimal("100.00"), Decimal("0.00")
                else:
                    female_pct = Decimal(str((gender_rate / 8) * 100))
                    male_pct = Decimal("100.00") - female_pct
                    gender_type = "MaleFemale"

                # 5. Mapeia o dicionário de estatísticas base
                stats_map = {s["stat"]["name"]: s["base_stat"] for s in raw_response["stats"]}
                
                # 6. Monta o payload limpo no formato do modelo do banco
                pokemon_data = {
                    "pokedex_number": raw_response["id"],
                    "name": raw_response["name"].capitalize(),
                    "species": species_genus,
                    "description": description,
                    "image_url": raw_response["sprites"]["other"]["official-artwork"]["front_default"] or "",
                    "height": Decimal(str(raw_response["height"])) / 10,  # Decímetros para metros
                    "weight": Decimal(str(raw_response["weight"])) / 10,  # Hectogramas para kg
                    "base_hp": stats_map.get("hp", 0),
                    "base_attack": stats_map.get("attack", 0),
                    "base_defense": stats_map.get("defense", 0),
                    "base_sp_attack": stats_map.get("special-attack", 0),
                    "base_sp_defense": stats_map.get("special-defense", 0),
                    "base_speed": stats_map.get("speed", 0),
                    "base_exp": raw_response["base_experience"] or 0,
                    "base_friendship": species_response["base_happiness"] or 0,
                    "growth_rate": species_response["growth_rate"]["name"],
                    "gender_type": gender_type,
                    "male_percentage": male_pct,
                    "female_percentage": female_pct,
                    "egg_cycles": species_response["hatch_counter"] or 0
                }

                # 7. Dispara a persistência através da interface do repositório
                self.poke_repo.save_pokemon(pokemon_data, type_ids)
                
            except Exception as e:
                print(f"Falha ao povoar o Pokémon ID {poke_id}: {str(e)}")