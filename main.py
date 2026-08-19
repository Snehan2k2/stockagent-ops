from src.data.ingestion import fetch_ohlcv
from src.config import DEFAULT_TICKER, START_DATE


def main():
    df = fetch_ohlcv(DEFAULT_TICKER, START_DATE)
    print(df.tail(10))
    print(f"\nFetched {len(df)} rows for {DEFAULT_TICKER}")


if __name__ == "__main__":
    main()
