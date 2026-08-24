import mlflow
import pandas as pd
from src.forecasting import backtest
from src.config import DEFAULT_TICKER

df = pd.read_parquet("feature_store/data/features.parquet")
df = df[df["ticker"] == DEFAULT_TICKER].sort_values("event_timestamp").reset_index(drop=True)

params = {"horizon": 5, "momentum_window": 14, "test_days": 200}

with mlflow.start_run(run_name=f"forecast_backtest_{DEFAULT_TICKER}"):
    mlflow.log_param("ticker", DEFAULT_TICKER)
    mlflow.log_params(params)
    results = backtest(df, **params)
    mlflow.log_metrics(results)
    print(f"Backtest results for {DEFAULT_TICKER}: {results}")
