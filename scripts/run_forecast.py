import pandas as pd
from src.forecasting import forecast_close
from src.config import DEFAULT_TICKER

df = pd.read_parquet("feature_store/data/features.parquet")
df = df[df["ticker"] == DEFAULT_TICKER].sort_values("event_timestamp")

forecast = forecast_close(df)
last_close = df["Close"].iloc[-1]
latest_rsi = df["RSI14"].iloc[-1]

print(f"{DEFAULT_TICKER} last close: {last_close:.2f} | RSI14: {latest_rsi:.2f}")
print(f"{len(forecast)}-day forecast: {forecast}")
