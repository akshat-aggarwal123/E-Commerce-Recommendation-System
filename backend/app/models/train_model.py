import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from joblib import dump
from ..utils.data_loader import DataLoader

class RecommendationModel:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.data_loader = DataLoader()

    def create_interaction_matrix(self):
        customers = self.data_loader.load_customer_data('backend/data/raw/customer_data_collection.csv')
        products = self.data_loader.load_product_data('backend/data/raw/product_recommendation_data.csv')
        
        interactions = []
        for _, customer in customers.iterrows():
            for _, product in products.iterrows():
                interactions.append({
                    'Customer_ID': customer['Customer_ID'],
                    'Product_ID': product['Product_ID'],
                    'Purchased': 1 if product['Subcategory'] in customer['Purchase_History'] else 0,
                    'Age': customer['Age'],
                    'Gender': customer['Gender'],
                    'Location': customer['Location'],
                    'Category': product['Category'],
                    'Brand': product['Brand'],
                    'Price': product['Price'],
                    'Ratings': product['Ratings']
                })
        return pd.DataFrame(interactions)

    def train(self):
        # Load data
        self.data_loader.load_customer_data('backend/data/raw/customer_data_collection.csv')
        self.data_loader.load_product_data('backend/data/raw/product_recommendation_data.csv')
        
        # Create features
        interaction_df = self.create_interaction_matrix()
        X = interaction_df.drop(['Customer_ID', 'Product_ID', 'Purchased'], axis=1)
        y = interaction_df['Purchased']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train model
        self.model.fit(X_train, y_train)
        dump(self.model, 'backend/models/recommendation_model.joblib')