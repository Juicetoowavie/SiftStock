import streamlit as st
import yfinance as yf
import pandas as pd

# Predefined stock list for simplicity (S&P 500 tickers or similar)
TICKERS = ['AAPL', 'MSFT', 'JNJ', 'NVDA', 'KO', 'PG', 'TSLA', 'AMZN', 'T', 'VZ', 'PEP', 'XOM', 'CVX']

# Simple user interface
st.title("Simple Stock Screener")
st.markdown("Filter stocks by your preferences. No finance degree needed!")

risk_level = st.selectbox("What level of risk are you comfortable with?", ["Low", "Medium", "High"])
sector_preference = st.selectbox("Interested in a specific sector?", ["Any", "Technology", "Healthcare", "Consumer", "Energy"])
dividends = st.checkbox("Prefer stocks that pay dividends?")

# Load and filter stock data
@st.cache_data
def load_stock_data(tickers):
    data = []
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        info = stock.info
        data.append({
            "Ticker": ticker,
            "Name": info.get("shortName", ""),
            "Sector": info.get("sector", ""),
            "Price": info.get("currentPrice", 0),
            "Beta": info.get("beta", 1),
            "Dividend Yield": info.get("dividendYield", 0) or 0,
        })
    return pd.DataFrame(data)

df = load_stock_data(TICKERS)

# Filtering logic
if sector_preference != "Any":
    df = df[df["Sector"].str.contains(sector_preference, na=False)]

if dividends:
    df = df[df["Dividend Yield"] > 0]

if risk_level == "Low":
    df = df[df["Beta"] < 1]
elif risk_level == "High":
    df = df[df["Beta"] > 1.2]

st.subheader("Matching Stocks")
st.dataframe(df.reset_index(drop=True))
