import csv
import random
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any

def generate_mock_data(file_path: str, num_records: int = 100) -> None:
    """
    Generate mock financial transactions with intentional data quality issues.
    
    Args:
        file_path (str): The path where the CSV file will be saved.
        num_records (int): Number of total records to generate.
    """
    
    headers: List[str] = ['transaction_id', 'date', 'account_id', 'amount', 'currency', 'type']
    
    transaction_types: List[str] = ['DEPOSIT', 'WITHDRAWAL', 'TRANSFER', 'PAYMENT']
    currencies: List[str] = ['EUR', 'USD', 'GBP', 'JPY'] # GBP and JPY will violate R4
    
    # Calculate a base date for generating random past dates
    today = datetime.now()
    
    data: List[Dict[str, Any]] = []
    
    for i in range(num_records):
        # Determine if this row should have an error (approx. 30% chance of having some error)
        has_error: bool = random.random() < 0.3
        
        # Valid base values
        txn_id = str(uuid.uuid4())
        txn_date = (today - timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d')
        account_id = f"ACC{random.randint(1000, 9999)}"
        amount = round(random.uniform(10.0, 5000.0), 2)
        currency = random.choice(['EUR', 'USD'])
        txn_type = random.choice(transaction_types)
        
        # Inject intentional errors based on the rules if has_error is True
        if has_error:
            error_type = random.choice(['R1_null_id', 'R1_null_date', 'R1_null_amount', 'R2_future_date', 'R3_negative_amount', 'R4_invalid_currency'])
            
            if error_type == 'R1_null_id':
                txn_id = None
            elif error_type == 'R1_null_date':
                txn_date = None
            elif error_type == 'R1_null_amount':
                amount = None
            elif error_type == 'R2_future_date':
                # Generate a date in the future
                txn_date = (today + timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d')
            elif error_type == 'R3_negative_amount':
                # Generate a negative amount
                amount = round(random.uniform(-1000.0, -10.0), 2)
            elif error_type == 'R4_invalid_currency':
                # Use a currency other than EUR or USD
                currency = random.choice(['GBP', 'JPY'])
                
        # Append the record
        data.append({
            'transaction_id': txn_id,
            'date': txn_date,
            'account_id': account_id,
            'amount': amount,
            'currency': currency,
            'type': txn_type
        })
        
    # Write to CSV
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)
        
    print(f"Successfully generated {num_records} mock transactions in '{file_path}'")

if __name__ == "__main__":
    output_file = "transactions_mock.csv"
    generate_mock_data(output_file, num_records=200)
