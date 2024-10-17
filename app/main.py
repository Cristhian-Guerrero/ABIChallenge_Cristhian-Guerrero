# app/main.py

from fastapi import FastAPI
from app.routers import predict
import logging
from app.db.database import engine
from app.db import models

app = FastAPI()

# Configure the logger
logging.basicConfig(level=logging.INFO)

# Create the database tables
models.Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Prediction API"}

# Include the predict router
app.include_router(predict.router)
