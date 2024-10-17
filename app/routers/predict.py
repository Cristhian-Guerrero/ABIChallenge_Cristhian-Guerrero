from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List
import pandas as pd
import logging
from app.utils.predictor import Predictor
from app.db.database import SessionLocal
from app.db.models import Prediction

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize the Predictor instance
predictor = Predictor(
    model_path='models/kmeans_model.joblib',
    scaler_path='models/scaler.joblib'
)

class InputData(BaseModel):
    Frequency: float
    MonetaryValue: float

def get_db():
    """
    Dependency to get the database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/predict')
def predict(data: List[InputData], db: SessionLocal = Depends(get_db)):
    """
    Endpoint to predict clusters for input data and store predictions in the database.

    Args:
        data (List[InputData]): List of input data instances.
        db (SessionLocal): Database session.

    Returns:
        dict: Dictionary containing the predicted clusters.
    """
    try:
        # Convert input data to DataFrame
        df = pd.DataFrame([item.model_dump() for item in data])
        logger.info(f"Received data: {df}")

        # Make predictions
        clusters = predictor.predict(df)

        # Store predictions in the database
        for idx, cluster in enumerate(clusters):
            prediction = Prediction(
                frequency=float(df.iloc[idx]['Frequency']),  # Convertir np.float64 a float
                monetary_value=float(df.iloc[idx]['MonetaryValue']),  # Convertir np.float64 a float
                cluster=int(cluster)
            )
            db.add(prediction)
        db.commit()

        # Return predictions
        return {'clusters': clusters.tolist()}
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return {'error': str(e)}
