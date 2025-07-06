import pandas as pd
from sqlalchemy import create_engine

# Step 1: Load the stock summary CSV
df = pd.read_csv("stock_summary.csv")

# Step 2: Create a SQLite database (file will be created in your folder)
engine = create_engine('sqlite:///stock_data.db')

# Step 3: Save the data to a table in the database
df.to_sql("stock_summary", engine, if_exists="replace", index=False)

print("✅ Data successfully saved to 'stock_data.db' in table 'stock_summary'")