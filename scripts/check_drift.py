import pandas as pd
from evidently import Report
from evidently.presets import DataDriftPreset

from src.config import DEFAULT_TICKER, FEATURES

df = pd.read_parquet("feature_store/data/features.parquet")
df = df[df["ticker"] == DEFAULT_TICKER].sort_values("event_timestamp").reset_index(drop=True)

current = df[FEATURES].tail(60)
reference = df[FEATURES].iloc[:-60]

report = Report([DataDriftPreset()])
result = report.run(current_data=current, reference_data=reference)
result.save_html(f"drift_report_{DEFAULT_TICKER}.html")

for m in result.dict()["metrics"]:
    print(m["metric_name"], "->", m["value"])