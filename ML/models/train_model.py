import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from joblib import dump
from utils.data_loader import DataLoader
import ast
from tqdm import tqdm

class RecommendationModel:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.data_loader = DataLoader()
        
        # Base directory of this script
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.customer_data_path = os.path.join(self.base_dir, '../data/customer_data_collection.csv')
        self.product_data_path = os.path.join(self.base_dir, '../data/raw/product_recommendation_data.csv')
        self.model_save_path = os.path.join(self.base_dir, '../models/recommendation_model.joblib')
        
        # Create directories if they don't exist
        os.makedirs(os.path.dirname(self.model_save_path), exist_ok=True)

    def safe_eval_list(self, x):
        """Safely convert string representation of lists to actual lists."""
        if isinstance(x, list):
            return x
        try:
            if isinstance(x, str) and (x.startswith('[') or x.startswith('(')):
                return ast.literal_eval(x)
            return []
        except:
            return []

    def create_interaction_matrix(self):
        # Load data with debug information
        print(f"Loading customer data from: {os.path.abspath(self.customer_data_path)}")
        print(f"Customer data file exists: {os.path.exists(self.customer_data_path)}")
        customers = self.data_loader.load_customer_data(self.customer_data_path)
        
        print(f"Loading product data from: {os.path.abspath(self.product_data_path)}")
        print(f"Product data file exists: {os.path.exists(self.product_data_path)}")
        products = self.data_loader.load_product_data(self.product_data_path)

        print("Products DataFrame shape:", products.shape)
        print("Customers DataFrame shape:", customers.shape)

        if products.empty:
            raise ValueError("Products DataFrame is empty. Please check the product data file.")
        
        if customers.empty:
            raise ValueError("Customers DataFrame is empty. Please check the customer data file.")

        print("Products DataFrame columns:", products.columns.tolist())
        print("Products DataFrame sample data:")
        print(products.head())

        # Debug Purchase_History
        print("Purchase_History sample (before conversion):")
        print(customers['Purchase_History'].head())
        print("First Purchase_History type:", type(customers['Purchase_History'].iloc[0]))

        # Ensure Purchase_History is properly converted to a list
        customers['Purchase_History'] = customers['Purchase_History'].apply(self.safe_eval_list)
        
        # Debug after conversion
        print("Purchase_History sample (after conversion):")
        print(customers['Purchase_History'].head())
        print("First Purchase_History type after conversion:", type(customers['Purchase_History'].iloc[0]))

        required_columns = ['Product_ID', 'Category', 'Subcategory', 'Price']
        for col in required_columns:
            if col not in products.columns:
                raise ValueError(f"Missing column: {col} in products DataFrame")

        # Create interaction matrix
        print("Creating interaction matrix...")
        
        # Option to limit data for testing
        # Uncomment the following lines to process a smaller dataset for testing
        # customers = customers.head(100)  # Use only first 100 customers
        # products = products.head(100)    # Use only first 100 products
        
        # Pre-process purchase history for all customers
        customer_purchase_histories = {}
        for i, customer in customers.iterrows():
            purchase_history = customer['Purchase_History']
            if not isinstance(purchase_history, list):
                purchase_history = []
            # Convert all elements to strings
            customer_purchase_histories[customer['Customer_ID']] = set(str(item) for item in purchase_history)
        
        # Create batches of customers to process
        batch_size = 100  # Adjust based on memory availability
        customer_batches = [customers[i:i+batch_size] for i in range(0, len(customers), batch_size)]
        
        all_interactions = []
        total_iterations = len(customer_batches)
        
        print(f"Processing {len(customers)} customers in {total_iterations} batches...")
        
        for batch_idx, customer_batch in enumerate(tqdm(customer_batches, desc="Processing customer batches")):
            batch_interactions = []
            
            for _, customer in customer_batch.iterrows():
                purchase_history_set = customer_purchase_histories[customer['Customer_ID']]
                
                for _, product in products.iterrows():
                    # Get subcategory safely and convert to string
                    subcategory = str(product['Subcategory'])
                    
                    batch_interactions.append({
                        'Customer_ID': customer['Customer_ID'],
                        'Product_ID': product['Product_ID'],
                        'Purchased': 1 if subcategory in purchase_history_set else 0,
                        'Age': float(customer['Age']),
                        'Gender': int(customer['Gender']),
                        'Location': int(customer['Location']),
                        'Category': int(product['Category']),
                        'Brand': int(product.get('Brand', 0)),
                        'Price': float(product['Price']),
                        'Ratings': float(product.get('Product_Rating', 0))
                    })
            
            # Convert batch to DataFrame and append to list
            batch_df = pd.DataFrame(batch_interactions)
            all_interactions.append(batch_df)
            
            # Print progress periodically
            if (batch_idx + 1) % 10 == 0 or batch_idx == 0:
                print(f"Completed batch {batch_idx + 1}/{total_iterations}. Current memory usage: {batch_df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        
        # Combine all batches
        print("Combining all interaction batches...")
        interaction_df = pd.concat(all_interactions, ignore_index=True)
        
        print(f"Interaction matrix created with shape: {interaction_df.shape}")
        print(f"Interaction matrix columns: {interaction_df.columns.tolist()}")
        print(f"Sample of interaction matrix:")
        print(interaction_df.head())
        
        # Check if there are any purchased items
        purchased_count = interaction_df['Purchased'].sum()
        print(f"Total purchased items in interaction matrix: {purchased_count}")
        print(f"Percentage of purchased items: {purchased_count/len(interaction_df)*100:.4f}%")
        
        return interaction_df

    def train(self):
        try:
            # Debug info about file paths
            print(f"Current working directory: {os.getcwd()}")
            print(f"Customer data path exists: {os.path.exists(self.customer_data_path)}")
            print(f"Product data path exists: {os.path.exists(self.product_data_path)}")
            
            # Create interaction matrix
            interaction_df = self.create_interaction_matrix()
            
            if interaction_df.empty:
                raise ValueError("Interaction DataFrame is empty. Cannot train model.")
            
            # Check if columns exist before dropping
            expected_columns = ['Customer_ID', 'Product_ID', 'Purchased']
            for col in expected_columns:
                if col not in interaction_df.columns:
                    raise ValueError(f"Column '{col}' not found in interaction DataFrame. Available columns: {interaction_df.columns.tolist()}")
            
            X = interaction_df.drop(expected_columns, axis=1)
            y = interaction_df['Purchased']

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            print("Training the model...")
            print(f"Training data shape: {X_train.shape}")
            print(f"Testing data shape: {X_test.shape}")
            print(f"Class distribution in training set: {y_train.value_counts().to_dict()}")
            
            # Train the model with progress indication
            print("Fitting the RandomForest model...")
            with tqdm(total=100, desc="Training model") as pbar:
                # Progress callback for RandomForest
                class ProgressCallback:
                    def __init__(self, pbar):
                        self.pbar = pbar
                        self.n_estimators = 100
                        self.current = 0
                    
                    def __call__(self, est):
                        self.current += 1
                        self.pbar.update(1)
                
                callback = ProgressCallback(pbar)
                self.model.fit(X_train, y_train, callback=callback)
            
            # Calculate and print accuracy
            train_accuracy = self.model.score(X_train, y_train)
            test_accuracy = self.model.score(X_test, y_test)
            print(f"Model trained successfully. Train accuracy: {train_accuracy:.4f}, Test accuracy: {test_accuracy:.4f}")
            
            # Feature importance
            feature_importance = pd.DataFrame({
                'Feature': X.columns,
                'Importance': self.model.feature_importances_
            }).sort_values('Importance', ascending=False)
            
            print("\nFeature Importance:")
            print(feature_importance)
            
            # Save model
            dump(self.model, self.model_save_path)
            print(f"Model saved to: {self.model_save_path}")
            
        except Exception as e:
            print(f"Error during model training: {str(e)}")
            import traceback
            traceback.print_exc()
            raise

if __name__ == "__main__":
    model = RecommendationModel()
    model.train()