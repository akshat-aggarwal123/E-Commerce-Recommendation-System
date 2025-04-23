import pandas as pd
from ast import literal_eval
from sklearn.preprocessing import LabelEncoder

class DataLoader:
    def __init__(self):
        self.customer_data = None
        self.product_data = None

    def load_customer_data(self, file_path):
        """Load and preprocess customer data."""
        df = pd.read_csv(file_path, header=None, names=[
            'Customer_ID', 'Age', 'Gender', 'Location',
            'Browsing_History', 'Purchase_History',
            'Customer_Segment', 'Avg_Order_Value',
            'Holiday', 'Season'
        ])

        # Helper function to safely evaluate literals
        def safe_literal_eval(x):
            try:
                return literal_eval(x) if pd.notnull(x) else []
            except (ValueError, SyntaxError):
                return []

        # Clean and process
        df['Browsing_History'] = df['Browsing_History'].apply(safe_literal_eval)
        df['Purchase_History'] = df['Purchase_History'].apply(safe_literal_eval)

        # Encode categorical features
        for col in ['Gender', 'Location', 'Customer_Segment']:
            df[col] = LabelEncoder().fit_transform(df[col].astype(str))

        self.customer_data = df
        return df

    def load_product_data(self, file_path):
        # Read the raw CSV file as a single string
        with open(file_path, 'r') as f:
            raw_data = f.read()

        # Split the raw data into individual rows
        rows = []
        current_row = []
        columns_per_row = 13  # Based on the number of columns in the schema

        # Process the raw data
        for value in raw_data.split(','):
            stripped_value = value.strip()
            if stripped_value.endswith(']'):  # Handle cases where lists are split across rows
                stripped_value = stripped_value.rstrip(']"').lstrip('"[')
            current_row.append(stripped_value)

            if len(current_row) == columns_per_row:
                rows.append(current_row)
                current_row = []

        # Drop incomplete rows
        if current_row:
            print(f"Dropped incomplete row: {current_row}")

        # Convert rows into a DataFrame
        df = pd.DataFrame(rows, columns=[
            'Product_ID', 'Category', 'Subcategory', 'Price',
            'Brand', 'Average_Rating_of_Similar_Products', 'Product_Rating',
            'Customer_Review_Sentiment_Score', 'Holiday', 'Season',
            'Geographical_Location', 'Similar_Product_List', 'Probability_of_Recommendation'
        ])

        # Drop rows with missing values
        df.dropna(inplace=True)

        # Ensure all required columns are present
        required_columns = [
            'Product_ID', 'Category', 'Subcategory', 'Price',
            'Brand', 'Average_Rating_of_Similar_Products', 'Product_Rating',
            'Customer_Review_Sentiment_Score', 'Holiday', 'Season',
            'Geographical_Location', 'Similar_Product_List'
        ]
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"The '{col}' column is missing in the loaded DataFrame.")

        # Clean and process
        def safe_literal_eval(x):
            try:
                return literal_eval(x) if pd.notnull(x) else []
            except (ValueError, SyntaxError):
                return []

        df['Similar_Product_List'] = df['Similar_Product_List'].apply(safe_literal_eval)
        df['Brand'] = df['Brand'].fillna('Unknown')

        # Encode categorical features
        for col in ['Category', 'Subcategory', 'Brand']:
            df[col] = LabelEncoder().fit_transform(df[col].astype(str))

        self.product_data = df
        return df