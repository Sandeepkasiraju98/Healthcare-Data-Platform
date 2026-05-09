import pandas as pd
from datetime import datetime

def extract(filepath):
    """Extract data from CSV"""
    print(f"[ETL] Extracting data from {filepath}...")
    df = pd.read_csv(filepath)
    print(f"[ETL] Extracted {len(df)} records")
    return df

def transform(df):
    """Clean and transform the dataset"""
    print("[ETL] Transforming data...")

    # Fix name casing
    df['Name'] = df['Name'].str.title().str.strip()

    # Parse dates
    df['Date of Admission'] = pd.to_datetime(df['Date of Admission'])
    df['Discharge Date'] = pd.to_datetime(df['Discharge Date'])

    # Calculate length of stay
    df['Length of Stay'] = (df['Discharge Date'] - df['Date of Admission']).dt.days

    # Standardize text columns
    for col in ['Gender', 'Medical Condition', 'Admission Type', 'Test Results', 'Medication']:
        df[col] = df[col].str.strip().str.title()

    # Round billing
    df['Billing Amount'] = df['Billing Amount'].round(2)

    # Add admission year and month
    df['Admission Year']  = df['Date of Admission'].dt.year
    df['Admission Month'] = df['Date of Admission'].dt.month_name()

    # Convert dates back to string for MongoDB
    df['Date of Admission'] = df['Date of Admission'].dt.strftime('%Y-%m-%d')
    df['Discharge Date']    = df['Discharge Date'].dt.strftime('%Y-%m-%d')

    print(f"[ETL] Transformation complete. {len(df)} records ready.")
    return df

def load(df, db):
    """Load data into MongoDB"""
    print("[ETL] Loading data into MongoDB...")
    collection = db['Patients']
    collection.drop()

    records = df.to_dict(orient='records')
    for i, record in enumerate(records, start=1):
        record['PatientID'] = i

    collection.insert_many(records)
    print(f"[ETL] Loaded {len(records)} records into MongoDB")
    return len(records)

def run_pipeline(filepath, db):
    """Run full ETL pipeline"""
    df = extract(filepath)
    df = transform(df)
    count = load(df, db)
    return count
