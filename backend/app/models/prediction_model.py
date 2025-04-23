from joblib import load
import os
from ..core.config import MODEL_PATH

class RecommendationModel:
    def __init__(self, model_path=MODEL_PATH):
        """
        Initialize the recommendation model.
        :param model_path: Path to the trained model file.
        """
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at {model_path}")
        
        # Load the pre-trained model
        self.model = load(model_path)

    def predict(self, X):
        """
        Predict recommendations based on input features.
        :param X: Input feature matrix (DataFrame or numpy array).
        :return: Model predictions.
        """
        return self.model.predict(X)

    def predict_proba(self, X):
        """
        Predict recommendation probabilities based on input features.
        :param X: Input feature matrix (DataFrame or numpy array).
        :return: Probability scores for each class.
        """
        return self.model.predict_proba(X)