# app.py
import streamlit as st
from model import train_and_predict

st.set_page_config(page_title="📈 Stock Price Predictor")

st.title("📊 Real-Time Stock Price Predictor")
ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, RELIANCE.NS)", value="AAPL")

if st.button("Predict Next Price"):
    with st.spinner("Training model and fetching data..."):
        df, pred = train_and_predict(ticker)
        st.line_chart(df["Close"])
        st.write("### 📌 Latest Price:", round(df['Close'].iloc[-1], 2))
        st.write("### 🔮 Predicted Next Price:", round(pred, 2))
