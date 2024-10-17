# app/utils/predictor.py

import joblib
import pandas as pd

class Predictor:
    """
    Class responsible for loading the machine learning model and making predictions.
    """

    def __init__(self, model_path: str, scaler_path: str):
        """
        Initialize the Predictor by loading the model and scaler.

        Args:
            model_path (str): Path to the trained model file.
            scaler_path (str): Path to the scaler file.
        """
        self.model = joblib.load(model_path)
        self.scaler = joblib.load(scaler_path)

    def preprocess(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocess the input data by scaling.

        Args:
            data (pd.DataFrame): Input data.

        Returns:
            pd.DataFrame: Scaled data.
        """
        # Ensure correct order of columns
        data = data[['Frequency', 'MonetaryValue']]
        # Scale data
        data_scaled = self.scaler.transform(data)
        return data_scaled

    def predict(self, data: pd.DataFrame) -> pd.Series:
        """
        Make predictions on the input data.

        Args:
            data (pd.DataFrame): Input data.

        Returns:
            pd.Series: Predicted clusters.
        """
        data_scaled = self.preprocess(data)
        clusters = self.model.predict(data_scaled)
        return pd.Series(clusters)
