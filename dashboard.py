import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
from alpha_vantage.fundamentaldata import FundamentalData
from stocknews import StockNews

# Page Title
st.title('📈 Stock Dashboard')

# Sidebar Inputs
ticker = st.sidebar.text_input('Enter Stock Ticker (e.g., MSFT)')
start_date = st.sidebar.date_input('Start Date')
end_date = st.sidebar.date_input('End Date')

# Check if ticker is entered
if not ticker:
    st.warning("Please enter a stock ticker to view data.")
    st.stop()

# Download Stock Data
@st.cache_data
def load_data(ticker, start, end):
    return yf.download(ticker, start=start, end=end)

data = load_data(ticker, start_date, end_date)

# Display Raw Data
st.subheader(f"Raw Data for {ticker}")
st.dataframe(data)

# Price Plot
fig = px.line(data, x=data.index, y='Adj Close', title=f"{ticker} Adjusted Closing Price")
st.plotly_chart(fig)

# Tabs for Details
pricing_data, fundamental_data, news = st.tabs(["📊 Pricing Data", "📚 Fundamental Data", "📰 Top 10 News"])

# Pricing Data Tab
with pricing_data:
    st.header('Price Movement')
    data2 = data.copy()
    data2['% Change'] = data2['Adj Close'].pct_change()
    st.dataframe(data2)

    annual_return = data2['% Change'].mean() * 252 * 100
    st.write(f"**Annual Return:** {annual_return:.2f}%")

    stdev = np.std(data2['% Change']) * np.sqrt(252)
    st.write(f"**Standard Deviation:** {stdev*100:.2f}%")

    if stdev > 0:
        st.write(f"**Risk-Adjusted Return (Sharpe Approx):** {annual_return / (stdev * 100):.2f}")
    else:
        st.write("Standard deviation is zero; Risk-Adjusted Return is undefined.")

# Fundamental Data Tab
with fundamental_data:
    st.header('Fundamental Data')

    try:
        key = 'OW1639LG3B5UCYL'  # API Key - do not share publicly
        fd = FundamentalData(key, output_format='pandas')

        st.subheader('Balance Sheet')
        balance_sheet = fd.get_balance_sheet_annual(ticker)[0]
        bs = balance_sheet.T[2:]
        bs.columns = balance_sheet.T.iloc[0]
        st.dataframe(bs)

        st.subheader('Income Statement')
        income_statement = fd.get_income_statement_annual(ticker)[0]
        is1 = income_statement.T[2:]
        is1.columns = income_statement.T.iloc[0]
        st.dataframe(is1)

        st.subheader('Cash Flow Statement')
        cash_flow = fd.get_cash_flow_annual(ticker)[0]
        cf = cash_flow.T[2:]
        cf.columns = cash_flow.T.iloc[0]
        st.dataframe(cf)

    except Exception as e:
        st.error(f"Error fetching fundamental data: {e}")

# News Tab
with news:
    st.header(f'Latest News for {ticker}')

    try:
        sn = StockNews(ticker, save_news=False)
        df_news = sn.read_rss()

        for i in range(min(10, len(df_news))):
            st.subheader(f"📰 News {i + 1}")
            st.write(f"**Date:** {df_news['published'][i]}")
            st.write(f"**Title:** {df_news['title'][i]}")
            st.write(f"**Summary:** {df_news['summary'][i]}")
            st.write(f"**Title Sentiment:** {df_news['sentiment_title'][i]}")
            st.write(f"**News Sentiment:** {df_news['sentiment_summary'][i]}")
            st.markdown("---")

    except Exception as e:
        st.error(f"Error fetching news: {e}")
