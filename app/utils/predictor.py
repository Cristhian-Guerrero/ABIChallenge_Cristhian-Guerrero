# app/utils/predictor.py

import joblib
import pandas as pd

class Predictor:
    """
    A class responsible for loading the machine learning model and making predictions.
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

    def predict(self, data: pd.DataFrame):
        """
        Make predictions on the input data.

        Args:
            data (pd.DataFrame): DataFrame containing the input features.

        Returns:
            np.ndarray: Array of predicted cluster labels.
        """
        # Ensure the correct order of columns
        data = data[['Frequency', 'MonetaryValue']]
        # Scale the input data
        data_scaled = self.scaler.transform(data)
        # Make predictions
        clusters = self.model.predict(data_scaled)
        return clusters
