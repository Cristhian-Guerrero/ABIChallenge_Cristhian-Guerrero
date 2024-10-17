# app/main.py

from fastapi import FastAPI
from app.routers import predict
from app.db.database import engine
from app.db import models

app = FastAPI(
    title="AB InBev MLOps Challenge API",
    version="0.1.0",
    description="API for predicting customer clusters based on RFM analysis."
)

# Crear las tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Welcome to the AB InBev MLOps Challenge API"}

app.include_router(predict.router)
