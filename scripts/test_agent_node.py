import requests

from src.agents.nodes import performance_analyst_node

data = requests.get("http://127.0.0.1:8000/predict/AAPL").json()

state = {
    "ticker": data["ticker"],
    "last_close": data["last_close"],
    "rsi14": data["rsi14"],
    "forecast": data["forecast"],
}

result = performance_analyst_node(state)
print(result["performance_analysis"])
