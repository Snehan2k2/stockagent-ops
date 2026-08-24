import pandas as pd


def forecast_close(df: pd.DataFrame, horizon: int = 5, momentum_window: int = 14) -> list[float]:
    """Deterministic forecast: extrapolate recent momentum, dampened when RSI is overbought/oversold."""
    closes = df["Close"].tail(momentum_window + 1).values
    daily_returns = (closes[1:] - closes[:-1]) / closes[:-1]
    avg_daily_return = daily_returns.mean()

    latest_rsi = df["RSI14"].iloc[-1]
    momentum_factor = 0.5 if (latest_rsi > 70 or latest_rsi < 30) else 1.0
    adjusted_return = avg_daily_return * momentum_factor

    price = df["Close"].iloc[-1]
    forecast = []
    for _ in range(horizon):
        price = price * (1 + adjusted_return)
        forecast.append(round(float(price), 2))
    return forecast


def backtest(df: pd.DataFrame, horizon: int = 5, momentum_window: int = 14, test_days: int = 200) -> dict:
    """Backtest the formula against real history: forecast forward from many past points, compare to what actually happened."""
    df = df.reset_index(drop=True)
    last_i = len(df) - 1 - horizon
    first_i = max(momentum_window, last_i - test_days + 1)

    errors = []
    for i in range(first_i, last_i + 1):
        history = df.iloc[: i + 1]
        actual_future = df["Close"].iloc[i + horizon]
        predicted = forecast_close(history, horizon=horizon, momentum_window=momentum_window)[-1]
        errors.append(abs(predicted - actual_future) / actual_future)

    return {"mape": sum(errors) / len(errors), "n_backtests": len(errors)}
