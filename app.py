# app.py
import streamlit as st
from model import train_and_predict
import pandas as pd

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
                        predicted_price = float(pred.item())
                    elif hasattr(pred, "__getitem__") and len(pred) == 1:
                        predicted_price = float(pred[0])
                    else:
                        predicted_price = float(pred)
                except Exception as e:
                    st.error(f"Error parsing predicted price: {e}")
                    st.stop()

                df = df.copy()

                # Flatten multi-index columns if needed
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = ['_'.join(col).strip() for col in df.columns.values]

                # Reset index if it caused duplicate 'index_' column
                if 'index_' in df.columns:
                    df = df.loc[:, ~df.columns.duplicated()]

                # Drop duplicate columns (keep first occurrence only)
                df = df.loc[:, ~df.columns.duplicated(keep='first')]

                # Rename first valid 'Close' column explicitly to avoid duplicates
                close_cols = [col for col in df.columns if 'Close' in col and col != 'Close']
                if close_cols:
                    df.rename(columns={close_cols[0]: 'Close'}, inplace=True)

                # Drop all duplicate columns again
                df = df.loc[:, ~df.columns.duplicated(keep='first')]
                for col in df.columns:
                    if 'Close' in col:
                        df.rename(columns={col: 'Close'}, inplace=True)

                df["Datetime"] = df.index
                df.set_index("Datetime", inplace=True)

                st.write("### 📄 Full Stock Price Data")
                st.dataframe(df)
                st.metric("📌 Latest Price", f"₹ {latest_price:.2f}")
                st.metric("🔮 Predicted Next Price", f"₹ {predicted_price:.2f}")
            else:
                st.error("No valid 'Close' price data returned. Try another ticker.")
        except Exception as e:
            st.error(f"⚠️ An error occurred: {e}")
