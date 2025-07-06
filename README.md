
# 📊 Data-Driven Stock Analysis: Organizing, Cleaning, and Visualizing Market Trends

## 🔍 Project Overview

This project analyzes the performance of **Nifty 50 stocks** over the past year using real-world financial data.  
The data was extracted from YAML files, transformed into structured CSVs, analyzed with Python and SQL, and visualized using **Streamlit** and **Power BI**.

---

## 🛠️ Tools & Technologies

- **Languages:** Python 3.x  
- **Libraries:** Pandas, PyYAML, Matplotlib, Seaborn, SQLite3  
- **Dashboard Tools:** Power BI, Streamlit  
- **Database:** SQLite  
- **Other:** Git, OS

---

## 📁 Folder Structure

```
project/
│
├── Dataset/                     # Original YAML files
├── symbol_csvs/                # Processed CSVs (one per stock)
├── all_returns.csv             # Daily & cumulative return per stock
├── monthly_returns.csv         # Monthly top 5 gainers/losers
├── correlation_matrix.csv      # For heatmap
├── stock_summary.csv           # Summary of all stocks
├── stock_data.db               # SQLite database
├── app.py                      # Streamlit app
├── PowerBI_Dashboard.pbix      # Power BI file (optional)
├── Nifty50_Project_Presentation.pptx
└── Nifty50_Final_Project_Report.pdf
```

---

## ⚙️ How to Run

### 1. Setup Environment

```bash
pip install pandas matplotlib seaborn streamlit pyyaml
```

### 2. Run Streamlit App

```bash
streamlit run app.py
```

---

## 📈 Features Included

✅ Top 10 Green & Red Stocks  
✅ Market Summary (Green/Red Count, Avg Price, Volume)  
✅ Volatility Chart (Standard Deviation of Daily Returns)  
✅ Sector-wise Average Return  
✅ 📈 Cumulative Return Chart for Top 5 Stocks  
✅ 🔗 Correlation Heatmap of Stock Prices  
✅ 📅 Monthly Gainers & Losers (Matrix Table)

---

## 🔗 Power BI Visuals

> Open `PowerBI_Dashboard.pbix` to view:

- Bar Chart: Top 10 Gainers/Losers  
- Avg Sector Performance  
- Monthly Gainers/Losers  
- Correlation Heatmap  
- Line Chart: Cumulative Returns  
- KPI Cards for Volume, Price, Green/Red Count

---

## 📚 Insights Gained

| Insight Category | Example |
|------------------|---------|
| Volatility       | ADANIENT & TATAMOTORS most volatile |
| Sector Leaders   | IT Sector showed highest avg return |
| Correlation      | INFY and TCS highly correlated |
| Monthly Trends   | Some stocks gained in Q2, dropped in Q4 |

---

## ✅ Author

- **Name**: [Your Name]  
- **Institution**: GUVI Project (Data Science Track)  
- **Project Duration**: 2025

---

## 📄 License

This project is for educational purposes only.
