# utils.py
import yfinance as yf
import pandas as pd

def fetch_multiple_stocks(tickers=None, period="30d", interval="1h"):
    if tickers is None:
        tickers = [
            "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS",
            "SBIN.NS", "LT.NS", "ITC.NS", "AXISBANK.NS", "BHARTIARTL.NS"
        ]

    all_data = []
    for ticker in tickers:
        df = yf.download(ticker, period=period, interval=interval)
        df.dropna(inplace=True)
        df["Ticker"] = ticker
        df["Next_Close"] = df["Close"].shift(-1)
        df.dropna(inplace=True)
        all_data.append(df)

    combined_df = pd.concat(all_data)
    return combined_df.reset_index()


