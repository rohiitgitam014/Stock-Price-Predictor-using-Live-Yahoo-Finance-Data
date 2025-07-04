# app.py
import streamlit as st
from model import train_and_predict

st.set_page_config(page_title="📈 Stock Price Predictor")

st.title("📊 Real-Time Stock Price Predictor")

# Dropdown menu for popular Indian stocks
ticker = st.selectbox("Select Stock Ticker", [
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS",
    "SBIN.NS", "LT.NS", "ITC.NS", "AXISBANK.NS", "BHARTIARTL.NS"
])

if st.button("Predict Next Price"):
    with st.spinner("Training model and fetching data..."):
        try:
            df, pred = train_and_predict(ticker)

            if "Close" in df.columns and not df["Close"].empty:
                try:
                    latest_price_val = df["Close"].iloc[-1]
                    latest_price = float(latest_price_val.values[0]) if hasattr(latest_price_val, 'values') else float(latest_price_val)
                except Exception as e:
                    st.error(f"Error parsing latest closing price: {e}")
                    st.stop()

                try:
                    if hasattr(pred, "item"):
