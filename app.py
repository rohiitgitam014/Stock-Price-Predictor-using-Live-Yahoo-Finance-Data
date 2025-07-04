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
                # Extract latest close price safely
                latest_price = float(df["Close"].iloc[-1])

                # Extract predicted value safely
                if hasattr(pred, "item"):
                    predicted_price = float(pred.item())
                elif hasattr(pred, "__getitem__") and len(pred) == 1:
                    predicted_price = float(pred[0])
                else:
                    predicted_price = float(pred)

                st.line_chart(df["Close"])
                st.metric("📌 Latest Price", f"₹ {latest_price:.2f}")
                st.metric("🔮 Predicted Next Price", f"₹ {predicted_price:.2f}")
            else:
                st.error("No valid 'Close' price data returned. Try another ticker.")
        except Exception as e:
            st.error(f"⚠️ An error occurred: {e}")
