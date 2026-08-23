from src.data.ingestion import fetch_ohlcv, save_to_feature_store
from src.config import DEFAULT_TICKER, START_DATE


def main():
    df = fetch_ohlcv(DEFAULT_TICKER, START_DATE)
    print(df.tail(10))
    print(f"\nFetched {len(df)} rows for {DEFAULT_TICKER}")

    save_to_feature_store(df, DEFAULT_TICKER)
    print(f"✅ Saved features for {DEFAULT_TICKER} to feature_store/data/features.parquet")


if __name__ == "__main__":
    main()
