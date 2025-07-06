import os
import yaml
import pandas as pd
from collections import defaultdict

# ✅ Use full absolute paths
output_folder = r'C:\Users\Lenovo\OneDrive\Documents\GUVI projects\Project 2\symbol_csvs4'

os.makedirs(output_folder, exist_ok=True)
symbol_data = defaultdict(list)

folder_path = r"C:\Users\Lenovo\OneDrive\Documents\GUVI projects\Project 2\Dataset"  # Use raw string or double backslashes
folder_names = os.listdir(folder_path)
file_list = []

print("Reading folder names to iterate")
for folder in folder_names:
        final_folder = folder_path + '\\' + folder
        for y_file_name in os.listdir(final_folder):
            if y_file_name.endswith('.yaml'):
                with open(os.path.join(final_folder, y_file_name), 'r', encoding='utf-8') as f:
                    daily_data = yaml.safe_load(f)
                    for stock in daily_data:
                        symbol_data[stock['Ticker']].append(stock)

print("Symbol data are collected, beginning to write to csv")
for symbol, records in symbol_data.items():
    df = pd.DataFrame(records)
    df.to_csv(os.path.join(output_folder, f"{symbol}.csv"), index=False)

print("files are written successfully")