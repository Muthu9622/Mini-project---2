import pandas as pd
import os
import numpy as np

# Step 1: Set the folder where your stock CSVs are saved
csv_folder = r'C:\Users\Lenovo\OneDrive\Documents\GUVI projects\Project 2\symbol_csvs4'

# Step 2: Load sector information (mapping file should have 'Ticker' and 'sector' columns)
sector_df = pd.read_csv(r"C:\Users\Lenovo\OneDrive\Documents\GUVI projects\Project 2\Sector_data.csv")  # Example: Ticker,sector

# Step 3: Make an empty list to collect summary info
summary_list = [ ]

for file in os.listdir(csv_folder):
    if file.endswith(".csv"):
        path = os.path.join(csv_folder, file)
        df = pd.read_csv(path)

        # 🧼 Clean column names: remove spaces, tabs, weird chars
        df.columns = df.columns.str.strip().str.replace('\ufeff', '')  # handles BOM if present

        # ✅ Confirm 'Ticker' exists
        if 'Ticker' not in df.columns:
            raise KeyError(f"'Ticker' column NOT found in {file}. Found columns: {df.columns.tolist()}")

        ticker = df['Ticker'].iloc[0]
        df['date'] = pd.to_datetime(df['date'])
        df.sort_values('date', inplace=True)

        df['daily_return'] = df['close'].pct_change()
        df['cumulative_return'] = (1 + df['daily_return']).cumprod()

        yearly_return = (df['close'].iloc[-1] - df['close'].iloc[0]) / df['close'].iloc[0]
        daily_std = df['daily_return'].std()
        annual_volatility = daily_std * (252 ** 0.5)
        avg_close = df['close'].mean()
        avg_volume = df['volume'].mean()

        summary_list.append({
            'Ticker': ticker,
            'yearly_return': yearly_return,
            'volatility': annual_volatility,
            'avg_close': avg_close,
            'avg_volume': avg_volume
        })

summary_df = pd.DataFrame(summary_list)

# 🧼 Clean sector_df columns too
summary_df = summary_df.merge(sector_df, on='Ticker', how='left')
summary_df.to_csv("stock_summary.csv", index=False)

print("✅ Done! 'stock_summary.csv' created with clean column handling.")