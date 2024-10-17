# app/routers/predict.py

from fastapi import APIRouter
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

@router.post('/predict')
def predict(data: List[InputData]):
    """
    Endpoint to predict the cluster(s) for one or multiple clients and store predictions in the database.

    Args:
        data (List[InputData]): A list of input data instances.

    Returns:
        dict: A dictionary containing the predicted cluster(s).
    """
    session = SessionLocal()
    try:
        # Convert the list of InputData to a DataFrame
        df = pd.DataFrame([item.model_dump() for item in data])
        logger.info(f"Received data: {df}")

        # Use the Predictor instance to make predictions
        clusters = predictor.predict(df)

        # Store predictions in the database
        for idx, cluster in enumerate(clusters):
            prediction = Prediction(
                frequency=df.iloc[idx]['Frequency'],
                monetary_value=df.iloc[idx]['MonetaryValue'],
                cluster=int(cluster)
            )
            session.add(prediction)
        session.commit()

        # Return the predictions as a list
        return {'clusters': clusters.tolist()}
    except Exception as e:
        session.rollback()
        logger.error(f"Prediction error: {e}")
        return {'error': str(e)}
    finally:
        session.close()