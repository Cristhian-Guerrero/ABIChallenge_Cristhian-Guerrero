# app/db/models.py

from sqlalchemy import Column, Integer, Float
from app.db.database import Base

class Prediction(Base):
    """
    Database model for storing predictions.
    """

    __tablename__ = 'predictions'

    id = Column(Integer, primary_key=True, index=True)
    frequency = Column(Float)
    monetary_value = Column(Float)
    cluster = Column(Integer)
