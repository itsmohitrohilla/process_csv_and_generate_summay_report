import pandas as pd
import os
import uuid

# Paths to the 'data' folders
PROCESSED_CSV_FOLDER = "data/processed_csv"
SUMMARY_REPORT_FOLDER = "data/summary_report"

def process_csv(file_path: str) -> str:
    """
    Process the uploaded CSV file by cleaning the data.
    Handle missing values and save the cleaned data to a new CSV file.
    """
    # Ensure the processed_csv folder exists
    os.makedirs(PROCESSED_CSV_FOLDER, exist_ok=True)
    
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Handling missing values
    if 'price' in df.columns:
        df['price'].fillna(df['price'].median(), inplace=True)
    if 'quantity_sold' in df.columns:
        df['quantity_sold'].fillna(df['quantity_sold'].median(), inplace=True)
    if 'rating' in df.columns and 'category' in df.columns:
        df['rating'] = df.groupby('category')['rating'].transform(lambda x: x.fillna(x.mean()))

    # Ensure numeric types
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df['quantity_sold'] = pd.to_numeric(df['quantity_sold'], errors='coerce')
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

    # Remove rows where any of these columns have NaN values
    df = df.dropna(subset=['price', 'quantity_sold', 'rating'])

    # Convert to integers
    df['price'] = df['price'].astype(int)
    df['quantity_sold'] = df['quantity_sold'].astype(int)
    df['rating'] = df['rating'].astype(int)

    # Generate a unique process ID
    process_id = str(uuid.uuid4())

    # Save the cleaned data to a new CSV file in the processed_csv folder
    cleaned_csv_path = os.path.join(PROCESSED_CSV_FOLDER, f"{process_id}.csv")
    df.to_csv(cleaned_csv_path, index=False)

    return process_id

def generate_summary_report(process_id: str) -> str:
    """
    Generate a summary report based on the cleaned CSV data.
    """
    # Ensure the summary_report folder exists
    os.makedirs(SUMMARY_REPORT_FOLDER, exist_ok=True)
    
    # Read the cleaned CSV file
    cleaned_csv_path = os.path.join(PROCESSED_CSV_FOLDER, f"{process_id}.csv")
    df = pd.read_csv(cleaned_csv_path)

    # Group by category to calculate total revenue and find the top product quantity sold
    grouped = df.groupby('category').agg(
        total_revenue=pd.NamedAgg(column='price', aggfunc='sum'),
        top_product_quantity_sold=pd.NamedAgg(column='quantity_sold', aggfunc='max')
    ).reset_index()

    # Find the top product for each category
    idx = df.groupby('category')['quantity_sold'].idxmax()
    top_products = df.loc[idx, ['category', 'product_name', 'quantity_sold']]

    # Merge to get the top product names into the grouped data
    summary = pd.merge(grouped, top_products, 
                       left_on=['category', 'top_product_quantity_sold'], 
                       right_on=['category', 'quantity_sold'], 
                       how='left')

    # Rename columns for clarity
    summary.rename(columns={'product_name': 'top_product'}, inplace=True)

    # Drop the redundant 'quantity_sold' column
    summary.drop(columns=['quantity_sold'], inplace=True)

    # Save the summary report to a new CSV file in the summary_report folder
    summary_csv_path = os.path.join(SUMMARY_REPORT_FOLDER, f"{process_id}_sr.csv")
    summary.to_csv(summary_csv_path, index=False)

    return summary_csv_path