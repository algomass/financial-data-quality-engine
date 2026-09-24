import pandas as pd
from typing import Tuple

def validate_transactions(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Validates a DataFrame of transactions against predefined Data Quality rules.
    
    Rules:
    - R1: transaction_id, date, amount must not be null.
    - R2: date must not be in the future.
    - R3: amount must be >= 0.
    - R4: currency must be 'EUR' or 'USD'.
    
    Args:
        df (pd.DataFrame): The input transactions data.
        
    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]: 
            - valid_df: DataFrame with valid records (no error_reason column)
            - error_df: DataFrame with invalid records and an error_reason column
    """
    # Create a working copy
    df = df.copy()
    
    # Initialize the error reason column
    df['error_reason'] = ""
    
    # ---------------------------------------------------------
    # Rule 1: transaction_id, date, amount non nulli
    # ---------------------------------------------------------
    r1_mask = df['transaction_id'].isna() | df['date'].isna() | df['amount'].isna()
    df.loc[r1_mask, 'error_reason'] += "R1: Missing mandatory fields. "
    
    # ---------------------------------------------------------
    # Rule 2: date non deve essere nel futuro
    # ---------------------------------------------------------
    # Convert 'date' to datetime for comparison, invalid dates become NaT
    current_date = pd.Timestamp.now().normalize()
    dates_converted = pd.to_datetime(df['date'], errors='coerce')
    r2_mask = dates_converted > current_date
    df.loc[r2_mask, 'error_reason'] += "R2: Date is in the future. "
    
    # ---------------------------------------------------------
    # Rule 3: amount deve essere >= 0
    # ---------------------------------------------------------
    # Convert 'amount' to numeric safely
    amounts_numeric = pd.to_numeric(df['amount'], errors='coerce')
    r3_mask = amounts_numeric < 0
    df.loc[r3_mask, 'error_reason'] += "R3: Amount is negative. "
    
    # ---------------------------------------------------------
    # Rule 4: currency deve essere 'EUR' o 'USD'
    # ---------------------------------------------------------
    r4_mask = ~df['currency'].isin(['EUR', 'USD'])
    df.loc[r4_mask, 'error_reason'] += "R4: Invalid currency. "
    
    # Clean up trailing spaces from the error reason string
    df['error_reason'] = df['error_reason'].str.strip()
    
    # ---------------------------------------------------------
    # Split DataFrames based on the presence of errors
    # ---------------------------------------------------------
    error_mask = df['error_reason'] != ""
    
    error_df = df[error_mask].copy()
    valid_df = df[~error_mask].copy()
    
    # The valid dataframe does not need the error_reason column
    valid_df = valid_df.drop(columns=['error_reason'])
    
    return valid_df, error_df

def main():
    input_file = "transactions_mock.csv"
    print(f"Loading data from '{input_file}'...")
    
    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"Error: '{input_file}' not found. Please run the mock data generator first.")
        return
        
    valid_df, error_df = validate_transactions(df)
    
    print("\n--- Data Quality Engine Results ---")
    print(f"Total records processed: {len(df)}")
    print(f"Valid records: {len(valid_df)}")
    print(f"Error records: {len(error_df)}\n")
    
    # Save partial results for inspection (Optional before STEP 3)
    valid_df.to_csv("valid_transactions.csv", index=False)
    error_df.to_csv("dq_error_log.csv", index=False)
    print("Intermediate files 'valid_transactions.csv' and 'dq_error_log.csv' generated for review.")

if __name__ == "__main__":
    main()
