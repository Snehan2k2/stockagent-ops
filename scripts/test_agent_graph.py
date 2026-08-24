import requests

from src.agents.graph import agent_graph

data = requests.get("http://127.0.0.1:8000/predict/AAPL").json()

initial_state = {
    "ticker": data["ticker"],
    "last_close": data["last_close"],
    "rsi14": data["rsi14"],
    "forecast": data["forecast"],
}

result = agent_graph.invoke(initial_state)
print(result["final_report"])
print("\nRecommendation:", result["recommendation"])
