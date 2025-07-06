import zipfile
import os

# Unzip the uploaded file into a working directory
zip_path = "/mnt/data/symbol_csvs4.zip"
extract_dir = "/mnt/data/symbol_csvs4"

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_dir)

# Confirm extraction by listing a few filenames
extracted_files = os.listdir(extract_dir)[:10]
extracted_files

# Drill down to the inner folder and list its contents
inner_folder = os.path.join(extract_dir, 'symbol_csvs4')
csv_files = glob(os.path.join(inner_folder, '*.csv'))

# Show a few file names to confirm contents
csv_files[:5]

# Generate all_returns.csv and monthly_returns.csv using the correct folder path

all_returns = []
monthly_returns = []

for file in csv_files:
    df = pd.read_csv(file)
    df.columns = df.columns.str.strip()

    if 'Ticker' not in df.columns or 'close' not in df.columns or 'date' not in df.columns:
        continue

    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['date', 'close'])
    df.sort_values('date', inplace=True)
    df['daily_return'] = df['close'].pct_change()
    df['cumulative_return'] = (1 + df['daily_return']).cumprod()
    df['month'] = df['date'].dt.to_period('M').astype(str)

    ticker = df['Ticker'].iloc[0]
    df['Ticker'] = ticker

    all_returns.append(df[['Ticker', 'date', 'close', 'daily_return', 'cumulative_return']])

    monthly = df.groupby('month')['close'].agg(['first', 'last']).reset_index()
    monthly['Ticker'] = ticker
    monthly['monthly_return'] = (monthly['last'] - monthly['first']) / monthly['first']
    monthly_returns.append(monthly[['Ticker', 'month', 'monthly_return']])

# Save to CSVs
all_returns_df = pd.concat(all_returns)
monthly_returns_df = pd.concat(monthly_returns)

all_returns_path = "/mnt/data/all_returns.csv"
monthly_returns_path = "/mnt/data/monthly_returns.csv"

all_returns_df.to_csv(all_returns_path, index=False)
monthly_returns_df.to_csv(monthly_returns_path, index=False)

all_returns_path, monthly_returns_path

# Create correlation_matrix.csv using all_returns_df

# Pivot data so that each column is a Ticker, each row a date
pivot_df = all_returns_df.pivot(index='date', columns='Ticker', values='close')

# Calculate percentage change and then correlation
returns_pct = pivot_df.pct_change()
correlation_matrix = returns_pct.corr()

# Save to CSV
correlation_matrix_path = "/mnt/data/correlation_matrix.csv"
correlation_matrix.to_csv(correlation_matrix_path)

correlation_matrix_path
