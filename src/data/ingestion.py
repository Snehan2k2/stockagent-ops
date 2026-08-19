import pandas as pd
import yfinance as yf


def rsi(series: pd.Series, period: int = 14) -> pd.Series:
    """Relative Strength Index (0-100): recent buying vs. selling pressure."""
    delta = series.diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=period).mean()
    rs = gain / loss
    return 100 - 100 / (1 + rs)


def macd(series: pd.Series, fast: int = 12, slow: int = 26) -> pd.Series:
    """MACD: fast moving average minus slow moving average, signals momentum shifts."""
    ema_fast = series.ewm(span=fast, adjust=False).mean()
    ema_slow = series.ewm(span=slow, adjust=False).mean()
    return ema_fast - ema_slow


def fetch_ohlcv(ticker: str, start: str) -> pd.DataFrame:
    df = yf.download(ticker, start=start, interval="1d", auto_adjust=True, progress=False)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df = df.reset_index().rename(columns={"Date": "date"})
    df = df[["date", "Open", "High", "Low", "Close", "Volume"]].dropna()
    df["RSI14"] = rsi(df["Close"])
    df["MACD"] = macd(df["Close"])
    df = df.dropna()
    return df
