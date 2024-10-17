from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.database import Base, DATABASE_URL

# Configurar cliente de pruebas
client = TestClient(app)

# Crear motor y sesión para la base de datos
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear tablas antes de realizar las pruebas
Base.metadata.create_all(bind=engine)

# Iniciar sesión y rollback después de cada test
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.rollback()  # Hacemos rollback para no afectar la base real
        db.close()

app.dependency_overrides['get_db'] = override_get_db

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
