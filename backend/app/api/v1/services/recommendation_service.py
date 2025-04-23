import pandas as pd
from sklearn.preprocessing import LabelEncoder
from joblib import load
from ..utils.data_loader import DataLoader
from ..core.config import MODEL_PATH

class RecommendationService:
    def __init__(self):
        self.model = load(MODEL_PATH)
        self.data_loader = DataLoader()
        self.customer_data = self.data_loader.load_customer_data('backend/data/raw/customer_data_collection.csv')
        self.product_data = self.data_loader.load_product_data('backend/data/raw/product_recommendation_data.csv')

    def generate_recommendations(self, customer_id, top_n=5):
        # Get customer details
        customer = self.customer_data[self.customer_data['Customer_ID'] == customer_id]
        if customer.empty:
            raise ValueError("Customer ID not found")
        
        customer = customer.iloc[0]
        features = {
            'Age': customer['Age'],
            'Gender': customer['Gender'],
            'Location': customer['Location'],
        }

        # Create interaction dataset
        interactions = []
        for _, product in self.product_data.iterrows():
            row = {
                'Age': features['Age'],
                'Gender': features['Gender'],
                'Location': features['Location'],
                'Category': product['Category'],
                'Brand': product['Brand'],
                'Price': product['Price'],
                'Ratings': product['Ratings']
            }
            interactions.append(row)
        
        interaction_df = pd.DataFrame(interactions)
        probs = self.model.predict_proba(interaction_df)[:, 1]
        
        # Combine with product data
        results = self.product_data.copy()
        results['Recommendation_Score'] = probs
        return results.sort_values('Recommendation_Score', ascending=False).head(top_n).to_dict(orient='records')