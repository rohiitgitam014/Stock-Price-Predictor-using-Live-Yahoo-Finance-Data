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
        df, pred = train_and_predict(ticker)
        st.line_chart(df["Close"])

        latest_price = round(df["Close"].iloc[-1], 2)
        predicted_price = round(pred, 2)

        st.metric("📌 Latest Price", f"₹ {latest_price}")
        st.metric("🔮 Predicted Next Price", f"₹ {predicted_price}")
