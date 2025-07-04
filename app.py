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

        if "Close" in df.columns and not df["Close"].empty:
            latest_price = df["Close"].values[-1]
            if hasattr(pred, "item"):
                predicted_price = pred.item()
            elif hasattr(pred, "__getitem__") and len(pred) == 1:
                predicted_price = pred[0]
            else:
                predicted_price = pred

            st.metric("📌 Latest Price", f"₹ {latest_price:.2f}")
            st.metric("🔮 Predicted Next Price", f"₹ {predicted_price:.2f}")
        else:
            st.error("No closing price data available. Please try another ticker.")
