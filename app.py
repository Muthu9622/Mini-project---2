
import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
from glob import glob

st.set_page_config(page_title="Nifty 50 Stock Dashboard", layout="wide")

st.title("📈 Nifty 50 Stock Performance Dashboard")

# Load summary data from SQLite
conn = sqlite3.connect("stock_data.db")
summary_df = pd.read_sql("SELECT * FROM stock_summary", conn)

# Market Summary
st.header("📌 Market Summary")
col1, col2, col3 = st.columns(3)
with col1:
    green = summary_df[summary_df['yearly_return'] > 0]
    st.metric("✅ Green Stocks", len(green))
with col2:
    red = summary_df[summary_df['yearly_return'] < 0]
    st.metric("❌ Red Stocks", len(red))
with col3:
    st.metric("📊 Avg Close Price", f"{summary_df['avg_close'].mean():.2f}")

st.metric("🔁 Avg Volume", f"{summary_df['avg_volume'].mean():,.0f}")

# Top Stocks
st.subheader("📈 Top 10 Green Stocks")
st.dataframe(green.sort_values("yearly_return", ascending=False).head(10))

st.subheader("📉 Top 10 Red Stocks")
st.dataframe(red.sort_values("yearly_return").head(10))

# Volatility
st.subheader("⚡ Top 10 Most Volatile Stocks")
top_vol = summary_df.sort_values("volatility", ascending=False).head(10)
fig1, ax1 = plt.subplots()
sns.barplot(data=top_vol, x="Ticker", y="volatility", ax=ax1)
ax1.set_title("Volatility (Standard Deviation of Daily Returns)")
st.pyplot(fig1)

# Sector-wise return
st.subheader("🏢 Sector-wise Average Yearly Return")
sector_group = summary_df.groupby("sector")["yearly_return"].mean().reset_index()
fig2, ax2 = plt.subplots()
sns.barplot(data=sector_group, x="sector", y="yearly_return", ax=ax2)
ax2.set_title("Average Yearly Return by Sector")
plt.xticks(rotation=45)
st.pyplot(fig2)

# Load individual stock CSVs for advanced analysis
csv_files = glob("symbol_csvs4/*.csv")
combined = []

for file in csv_files:
    df = pd.read_csv(file)
    df.columns = df.columns.str.strip()
    if 'Ticker' not in df.columns or 'close' not in df.columns or 'date' not in df.columns:
        continue
    df = df[['Ticker', 'date', 'close']].copy()
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['date'])
    df.sort_values('date', inplace=True)
    df['daily_return'] = df['close'].pct_change()
    df['cumulative_return'] = (1 + df['daily_return']).cumprod()
    combined.append(df)

if combined:
    all_returns = pd.concat(combined)

    # Cumulative Return Chart
    st.subheader("📈 Cumulative Return Over Time (Top 5 Stocks)")
    top5_tickers = summary_df.sort_values("yearly_return", ascending=False)['Ticker'].head(5).tolist()
    fig3, ax3 = plt.subplots()
    for ticker in top5_tickers:
        df_plot = all_returns[all_returns['Ticker'] == ticker]
        ax3.plot(df_plot['date'], df_plot['cumulative_return'], label=ticker)
    ax3.set_title("Top 5 Performing Stocks (Cumulative Return)")
    ax3.legend()
    st.pyplot(fig3)

    # Correlation Heatmap
    st.subheader("🔗 Correlation Heatmap of Closing Prices")
    pivot_df = all_returns.pivot(index='date', columns='Ticker', values='close')
    corr_matrix = pivot_df.pct_change().corr()
    fig4, ax4 = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", ax=ax4)
    ax4.set_title("Stock Price Correlation")
    st.pyplot(fig4)

    # Monthly Gainers & Losers
    st.subheader("📅 Monthly Top 5 Gainers and Losers")
    all_returns['month'] = all_returns['date'].dt.to_period('M').astype(str)
    monthly_returns = all_returns.groupby(['Ticker', 'month'])['close'].agg(['first', 'last']).reset_index()
    monthly_returns['monthly_return'] = (monthly_returns['last'] - monthly_returns['first']) / monthly_returns['first']

    months = monthly_returns['month'].unique().tolist()
    for month in months:
        st.markdown(f"### 📆 {month}")
        month_df = monthly_returns[monthly_returns['month'] == month]
        top5 = month_df.sort_values('monthly_return', ascending=False).head(5)
        bottom5 = month_df.sort_values('monthly_return').head(5)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Top 5 Gainers**")
            st.dataframe(top5[['Ticker', 'monthly_return']])
        with col2:
            st.markdown("**Top 5 Losers**")
            st.dataframe(bottom5[['Ticker', 'monthly_return']])
else:
    st.warning("⚠️ No valid CSVs found in 'symbol_csvs/' or required columns are missing.")

conn.close()
