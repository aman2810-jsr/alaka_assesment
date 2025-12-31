import pandas as pd
import os
from datetime import datetime



def generate_candles(filename: str):
    file_path = f"data/{filename}"
    if not file_path.endswith(".csv"):
        file_path += ".csv"
    
    target_date = "2024-01-10"
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        
        df['date'] = pd.to_datetime(df['date'])
        
        filtered_df = df[df['date'].dt.date == pd.to_datetime(target_date).date()]
        
        filtered_df = filtered_df.set_index('date')
        
        candles = filtered_df.resample('5min').agg({
            'open': 'first',    
            'high': 'max',      
            'low': 'min',       
            'close': 'last',    
            'volume': 'sum'     
        }).dropna()
        
        candles = candles.reset_index()
        
        os.makedirs("5min_candles", exist_ok=True)
        
        output_filename = filename if filename.endswith(".csv") else f"{filename}.csv"
        candles.to_csv(f"5min_candles/{output_filename}", index=False)
        print(f"Generated 5min candles for {filename} -> saved to 5min_candles/{output_filename} ({len(candles)} candles)")
    else:
        print(f"ERROR: Could not find file at {os.path.abspath(file_path)}")


def generate_fibonacci_pivot(filename: str):
    file_path = f"data/{filename}"
    if not file_path.endswith(".csv"):
        file_path += ".csv"
    
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        
        df['date'] = pd.to_datetime(df['date'])
        
        df['date_only'] = df['date'].dt.date
        
        pivot_data = []
        for date, group in df.groupby('date_only'):
            high = group['high'].max()
            low = group['low'].min()
            open_val = group['open'].iloc[0]  
            close = group['close'].iloc[-1]  
            
            p = (high + low + close) / 3
            
            hl_range = high - low
            
            r1 = p + 0.382 * hl_range
            r2 = p + 0.618 * hl_range
            r3 = p + hl_range
            s1 = p - 0.382 * hl_range
            s2 = p - 0.618 * hl_range
            s3 = p - hl_range
            
            pivot_data.append({
                'date': date,
                'open': round(open_val, 4),
                'high': round(high, 4),
                'low': round(low, 4),
                'close': round(close, 4),
                'P': round(p, 4),
                'R1': round(r1, 4),
                'R2': round(r2, 4),
                'R3': round(r3, 4),
                'S1': round(s1, 4),
                'S2': round(s2, 4),
                'S3': round(s3, 4)
            })
        
        pivot_df = pd.DataFrame(pivot_data)
        
        os.makedirs("fibonacci_pivot", exist_ok=True)
        
        output_filename = filename if filename.endswith(".csv") else f"{filename}.csv"
        pivot_df.to_csv(f"fibonacci_pivot/{output_filename}", index=False)
        print(f"Generated Fibonacci pivot levels for {filename} -> saved to fibonacci_pivot/{output_filename} ({len(pivot_df)} dates)")
