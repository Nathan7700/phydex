import pytest
from fastapi.testclient import TestClient
from src.infrastructure.api.main import app

client = TestClient(app)

def test_login_success():
    # Enviando exatamente os campos padrões que o TrainerLoginSchema exige
    payload = {
        "email": "treinador_ash@exemplo.com", 
        "password": "senha_correta"
    }
    response = client.post("/auth/login", json=payload)
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_wrong_password():
    # Força o erro de validação de senha que o caso de uso espera ("123")
    payload = {
        "email": "treinador_ash@exemplo.com", 
        "password": "123"
    }
    response = client.post("/auth/login", json=payload)
    assert response.status_code == 400

def test_create_team_and_limit_validation():
    # 3 Pokémon = Sucesso
    valid_payload = {"name": "Time Campeao", "pokemon_ids": [25, 4, 7]}
    response = client.post("/teams/", json=valid_payload)
    assert response.status_code == 201
    
    # 7 Pokémon = Deve falhar no middleware (Limite estourado)
    invalid_payload = {"name": "Time Errado", "pokemon_ids": [1, 2, 3, 4, 5, 6, 7]}
    response_invalid = client.post("/teams/", json=invalid_payload)
    assert response_invalid.status_code == 400
    assert response_invalid.json()["message"] == "Uma equipe não pode ter mais de 6 Pokémon."