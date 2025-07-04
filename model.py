# model.py
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from utils import fetch_stock_data

def train_and_predict(ticker="AAPL"):
    df = fetch_stock_data(ticker)
    X = df[["Open", "High", "Low", "Close", "Volume"]]
    y = df["Next_Close"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    latest = df.iloc[-1][["Open", "High", "Low", "Close", "Volume"]].values.reshape(1, -1)
    prediction = model.predict(latest)[0]
    
    return df, prediction
