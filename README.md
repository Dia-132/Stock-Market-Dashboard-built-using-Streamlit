# Stock-Market-Dashboard-built-using-Streamlit



This project is a **web-based Stock Market Dashboard** built using **Streamlit**. It allows users to explore historical stock prices, fundamental financial data, and the latest news for any listed stock by entering its ticker symbol.

---

## Features

- **Stock Price Chart**: Interactive line chart of the stock's adjusted closing prices over a selected date range.
- **Pricing Data Analysis**:
  - Daily percentage changes
  - Annual return
  - Standard deviation
  - Risk-adjusted return (Sharpe ratio approximation)
- **Fundamental Data**:
  - Balance Sheet
  - Income Statement
  - Cash Flow Statement  
  *(fetched using Alpha Vantage API)*
- **Top 10 News Articles**:
  - Titles, summaries, publication dates
  - Sentiment analysis for each article  
  *(fetched using StockNews API)*

---

## Requirements

Install the required Python packages using:

```bash
pip install -r requirements.txt
