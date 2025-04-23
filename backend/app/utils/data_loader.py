import pandas as pd
from ast import literal_eval
from sklearn.preprocessing import LabelEncoder

class DataLoader:
    def __init__(self):
        self.customer_data = None
        self.product_data = None

    def load_customer_data(self, file_path):
        df = pd.read_csv(file_path, header=None, names=[
            'Customer_ID', 'Age', 'Gender', 'Location', 
            'Browsing_History', 'Purchase_History', 
            'Customer_Segment', 'Avg_Order_Value', 
            'Holiday', 'Season'
        ])
        
        # Clean and process
        df['Browsing_History'] = df['Browsing_History'].apply(lambda x: literal_eval(x) if pd.notnull(x) else [])
        df['Purchase_History'] = df['Purchase_History'].apply(lambda x: literal_eval(x) if pd.notnull(x) else [])
        
        # Encode categorical features
        for col in ['Gender', 'Location', 'Customer_Segment']:
            df[col] = LabelEncoder().fit_transform(df[col].astype(str))
        
        self.customer_data = df
        return df

    def load_product_data(self, file_path):
        df = pd.read_csv(file_path, header=None, names=[
            'Product_ID', 'Category', 'Subcategory', 'Price', 
            'Brand', 'Ratings', 'RatingsCount', 'Discount', 
            'Holiday', 'Season', 'Country', 'Features'
        ])
        
        # Process features
        df['Features'] = df['Features'].apply(lambda x: literal_eval(x) if pd.notnull(x) else [])
        df['Brand'] = df['Brand'].fillna('Unknown')
        
        # Encode categorical features
        for col in ['Category', 'Subcategory', 'Brand']:
            df[col] = LabelEncoder().fit_transform(df[col].astype(str))
        
        self.product_data = df
        return df