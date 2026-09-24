import pandas as pd
from sqlalchemy import create_engine
from typing import Optional

def setup_and_load_db(
    valid_df: pd.DataFrame, 
    error_df: pd.DataFrame, 
    db_url: str = "sqlite:///financial_data.db"
) -> None:
    """
    Sets up the SQLite database connection using SQLAlchemy and loads the
    DataFrames into their respective tables.
    
    Args:
        valid_df (pd.DataFrame): DataFrame containing valid transactions.
        error_df (pd.DataFrame): DataFrame containing rejected transactions.
        db_url (str): The database URL (defaults to a local SQLite file).
    """
    
    print(f"Connecting to database at: {db_url}")
    # Create the SQLAlchemy engine for SQLite
    engine = create_engine(db_url)
    
    # In a production environment with pandas, to_sql coupled with an SQLAlchemy 
    # engine is the most efficient and robust way for bulk loading.
    
    # 1. Load Valid Transactions
    # We use if_exists='replace' to easily re-run our pipeline in this portfolio project.
    # In a real DW scenario, this would likely be 'append' with a deduplication step.
    valid_df.to_sql(
        name='valid_transactions',
        con=engine,
        if_exists='replace',
        index=False
    )
    print(f"-> Successfully loaded {len(valid_df)} records into 'valid_transactions'.")
    
    # 2. Load Error Logs
    error_df.to_sql(
        name='dq_error_log',
        con=engine,
        if_exists='replace',
        index=False
    )
    print(f"-> Successfully loaded {len(error_df)} records into 'dq_error_log'.")

def main():
    try:
        # Load the intermediate CSV files generated 
        print("Reading intermediate CSV files...")
        valid_df = pd.read_csv('valid_transactions.csv')
        error_df = pd.read_csv('dq_error_log.csv')
        
        # Load into SQLite
        setup_and_load_db(valid_df, error_df)
        
    except FileNotFoundError as e:
        print(f"Error: Could not find input files. Did you run STEP 2? Details: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
