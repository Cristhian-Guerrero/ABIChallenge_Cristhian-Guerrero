# tests/test_predict.py

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_predict_single():
    response = client.post(
        "/predict",
        json=[{"Frequency": 5, "MonetaryValue": 1000.0}],
    )
    assert response.status_code == 200
    assert "clusters" in response.json()
    assert isinstance(response.json()["clusters"], list)
    assert len(response.json()["clusters"]) == 1

def test_predict_batch():
    response = client.post(
        "/predict",
        json=[
            {"Frequency": 5, "MonetaryValue": 1000.0},
            {"Frequency": 10, "MonetaryValue": 500.0},
            {"Frequency": 2, "MonetaryValue": 1500.0}
        ],
    )
    assert response.status_code == 200
    assert "clusters" in response.json()
    assert isinstance(response.json()["clusters"], list)
    assert len(response.json()["clusters"]) == 3

def test_predict_invalid_input():
    response = client.post(
        "/predict",
        json=[{"Frequency": "invalid", "MonetaryValue": "invalid"}],
    )
    assert response.status_code == 422  # Validation error

def test_predict_missing_field():
    response = client.post(
        "/predict",
        json=[{"Frequency": 5}],
    )
    assert response.status_code == 422  # Validation error
