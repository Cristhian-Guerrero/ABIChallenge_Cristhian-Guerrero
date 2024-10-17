# app/db/models.py

from sqlalchemy import Column, Integer, Float
from app.db.database import Base

class Prediction(Base):
    """
    SQLAlchemy model for storing prediction results in the database.
    """
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    frequency = Column(Float, nullable=False)
    monetary_value = Column(Float, nullable=False)
    cluster = Column(Integer, nullable=False)
