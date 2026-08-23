from feast import FeatureStore
from src.config import DEFAULT_TICKER

store = FeatureStore(repo_path="feature_store")

online = store.get_online_features(
    features=[
        "stock_features:Open",
        "stock_features:High",
        "stock_features:Low",
        "stock_features:Close",
        "stock_features:Volume",
        "stock_features:RSI14",
        "stock_features:MACD",
    ],
    entity_rows=[{"ticker": DEFAULT_TICKER}],
).to_dict()

print(f"Online (Redis) features for {DEFAULT_TICKER}:")
for k, v in online.items():
    print(f"  {k}: {v}")
