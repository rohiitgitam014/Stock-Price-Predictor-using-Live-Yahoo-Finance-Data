# utils.py
import yfinance as yf
import pandas as pd

def fetch_stock_data(ticker="RELIANCE.NS", period="30d", interval="1h"):
    df = yf.download(ticker, period=period, interval=interval)
    df.dropna(inplace=True)
    df["Next_Close"] = df["Close"].shift(-1)
    df.dropna(inplace=True)
    return df

