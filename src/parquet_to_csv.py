import pandas as pd
import os
from pathlib import Path

source_dir = r"C:\Users\aj281\Desktop\data\candles\BANKNIFTY\2024-01-10"
output_dir = r"C:\Users\aj281\Desktop\data\data"

os.makedirs(output_dir, exist_ok=True)

parquet_files = [f for f in os.listdir(source_dir) if f.endswith('.parquet')]

for parquet_file in parquet_files:
    parquet_path = os.path.join(source_dir, parquet_file)
    df = pd.read_parquet(parquet_path)
    
    csv_filename = parquet_file.replace('.parquet', '.csv')
    csv_path = os.path.join(output_dir, csv_filename)
    
    df.to_csv(csv_path, index=False)
    print(f"Converted: {parquet_file} -> {csv_filename}")

print(f"\nConversion complete! {len(parquet_files)} files converted and saved to {output_dir}")
