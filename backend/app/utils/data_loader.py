import pandas as pd
import os
import ast
from sklearn.preprocessing import LabelEncoder

class DataLoader:
    def __init__(self):
        self.customer_data = None
        self.product_data = None
        
    def safe_literal_eval(self, x):
        """Safely convert string representation of lists to actual lists."""
        try:
            if pd.isna(x) or x == '':
                return []
            if isinstance(x, list):
                return x
            result = ast.literal_eval(str(x))
            # Ensure result is a list
            if isinstance(result, list):
                return result
            else:
                return [str(result)]
        except Exception as e:
            print(f"Error parsing value '{x}': {str(e)}")
            return []
        
    def load_customer_data(self, file_path):
        """Load and preprocess customer data."""
        try:
            # First try to load with standard pandas read_csv
            try:
                df = pd.read_csv(file_path)
                print("Successfully loaded customer data with automatic header detection")
            except:
                # If that fails, try with explicit column names
                df = pd.read_csv(
                    file_path,
                    header=None,
                    names=[
                        'Customer_ID', 'Age', 'Gender', 'Location',
                        'Browsing_History', 'Purchase_History',
                        'Customer_Segment', 'Avg_Order_Value',
                        'Holiday', 'Season'
                    ],
                    dtype=str,
                    on_bad_lines='skip'
                )
                print("Loaded customer data with explicit column names")
            
            # Show file details
            print(f"Customer file size: {os.path.getsize(file_path)} bytes")
            print(f"Customer data loaded with {df.shape[0]} rows and {df.shape[1]} columns")
            print(f"Customer columns: {df.columns.tolist()}")
            
            if df.empty:
                print("Warning: Customer DataFrame is empty!")
                return df
                
            # Handle list columns safely
            if 'Browsing_History' in df.columns:
                df['Browsing_History'] = df['Browsing_History'].apply(self.safe_literal_eval)
            else:
                print("Warning: 'Browsing_History' column not found")
                df['Browsing_History'] = [[]] * len(df)
                
            if 'Purchase_History' in df.columns:
                df['Purchase_History'] = df['Purchase_History'].apply(self.safe_literal_eval)
            else:
                print("Warning: 'Purchase_History' column not found")
                df['Purchase_History'] = [[]] * len(df)
            
            # Convert numeric columns
            if 'Age' in df.columns:
                df['Age'] = pd.to_numeric(df['Age'], errors='coerce').fillna(0)
            
            # Encode categorical columns
            for col in ['Gender', 'Location', 'Customer_Segment']:
                if col in df.columns:
                    df[col] = LabelEncoder().fit_transform(df[col].astype(str))
                else:
                    print(f"Warning: '{col}' column not found")
                    df[col] = 0
            
            self.customer_data = df
            return df
            
        except Exception as e:
            print(f"Error loading customer data: {str(e)}")
            import traceback
            traceback.print_exc()
            # Return empty DataFrame with required columns
            columns = ['Customer_ID', 'Age', 'Gender', 'Location', 'Browsing_History', 'Purchase_History']
            return pd.DataFrame(columns=columns)
    
    def load_product_data(self, file_path):
        """Load and preprocess product data."""
        try:
            # Try to load the file with automatic header detection first
            try:
                df = pd.read_csv(file_path)
                print("Successfully loaded product data with automatic header detection")
            except Exception as auto_error:
                print(f"Automatic header detection failed: {str(auto_error)}")
                
                # If that fails, try explicit approach
                expected_columns = [
                    'Product_ID', 'Category', 'Subcategory', 'Price',
                    'Brand', 'Average_Rating_of_Similar_Products',
                    'Product_Rating', 'Customer_Review_Sentiment_Score',
                    'Holiday', 'Season', 'Geographical_Location',
                    'Similar_Product_List', 'Probability_of_Recommendation'
                ]
                
                try:
                    # Try to read with no header
                    df = pd.read_csv(
                        file_path,
                        header=None,
                        names=expected_columns,
                        dtype=str,
                        skip_blank_lines=True,
                        on_bad_lines='skip'
                    )
                    print("Loaded product data with explicit column names and no header")
                except Exception as e:
                    print(f"Error loading product data with no header: {str(e)}")
                    # Last resort approach - try reading raw file and parse manually
                    try:
                        with open(file_path, 'r') as f:
                            lines = f.readlines()
                        
                        print(f"Raw file contains {len(lines)} lines")
                        if len(lines) > 0:
                            print(f"First line example: {lines[0]}")
                        
                        # Create empty DataFrame with expected columns
                        df = pd.DataFrame(columns=expected_columns)
                        return df
                    except Exception as raw_error:
                        print(f"Raw file reading failed: {str(raw_error)}")
                        return pd.DataFrame(columns=expected_columns)
            
            # Print file information
            print(f"Product file size: {os.path.getsize(file_path)} bytes")
            print(f"Product data loaded with {df.shape[0]} rows and {df.shape[1]} columns")
            print(f"Product columns: {df.columns.tolist()}")
            
            if df.empty:
                print("Warning: Product DataFrame is empty!")
                return df
            
            # Ensure required columns exist
            required_columns = ['Product_ID', 'Category', 'Subcategory', 'Price']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                print(f"Warning: Missing required columns: {missing_columns}")
                for col in missing_columns:
                    df[col] = 'Unknown' if col != 'Price' else 0.0
            
            # Drop rows where Product_ID is missing or empty
            if 'Product_ID' in df.columns:
                original_count = len(df)
                df = df[df['Product_ID'].notna() & (df['Product_ID'].str.strip() != '')]
                if len(df) < original_count:
                    print(f"Dropped {original_count - len(df)} rows with missing Product_ID")
                df.reset_index(drop=True, inplace=True)
            
            # Safely parse the list-column if it exists
            if 'Similar_Product_List' in df.columns:
                df['Similar_Product_List'] = df['Similar_Product_List'].apply(self.safe_literal_eval)
            
            # Convert numeric columns (coerce errors to NaN)
            numeric_columns = [
                'Price', 'Average_Rating_of_Similar_Products',
                'Product_Rating', 'Customer_Review_Sentiment_Score',
                'Probability_of_Recommendation'
            ]
            
            for col in numeric_columns:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
            # Fill any missing Brand
            if 'Brand' in df.columns:
                df['Brand'] = df['Brand'].fillna('Unknown')
            else:
                df['Brand'] = 'Unknown'
            
            # Encode categorical fields
            for col in ['Category', 'Subcategory', 'Brand']:
                if col in df.columns:
                    df[col] = LabelEncoder().fit_transform(df[col].astype(str))
                else:
                    df[col] = 0
            
            self.product_data = df
            return df
            
        except Exception as e:
            print(f"Error in load_product_data: {str(e)}")
            import traceback
            traceback.print_exc()
            columns = ['Product_ID', 'Category', 'Subcategory', 'Price', 'Brand', 'Product_Rating']
            return pd.DataFrame(columns=columns)