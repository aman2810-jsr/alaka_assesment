import os
from pathlib import Path
from candles_utils import generate_candles, generate_fibonacci_pivot

DATA_DIR = "data"

def main():
    csv_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.csv')]
    
    for csv_file in csv_files:
        filename = csv_file.replace('.csv', '')
        generate_candles(filename)
        generate_fibonacci_pivot(filename)

if __name__ == "__main__":
    main()
