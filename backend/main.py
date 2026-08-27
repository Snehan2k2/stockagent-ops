import hashlib
import json

import pandas as pd
import redis
from fastapi import FastAPI, HTTPException, Request

from src.agents.graph import agent_graph
from src.forecasting import forecast_close

from src.agents.semantic_cache import find_similar
from src.agents.semantic_cache import store as store_semantic

app = FastAPI(title="build-stock-agent-ops")
redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

from prometheus_fastapi_instrumentator import Instrumentator
Instrumentator().instrument(app).expose(app)

RATE_LIMIT = 5
RATE_WINDOW_SECONDS = 30


def check_rate_limit(client_ip: str):
    key = f"ratelimit:predict:{client_ip}"
    current = redis_client.incr(key)
    if current == 1:
        redis_client.expire(key, RATE_WINDOW_SECONDS)
    if current > RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Try again shortly.")


def get_prediction(ticker: str) -> dict:
    df = pd.read_parquet("feature_store/data/features.parquet")
    df = df[df["ticker"] == ticker].sort_values("event_timestamp").reset_index(drop=True)

    if df.empty:
        raise HTTPException(status_code=404, detail=f"No feature data for {ticker}")

    forecast = forecast_close(df)
    return {
        "ticker": ticker,
        "last_close": float(df["Close"].iloc[-1]),
        "rsi14": float(df["RSI14"].iloc[-1]),
        "forecast": forecast,
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/predict/{ticker}")
def predict(ticker: str, request: Request):
    check_rate_limit(request.client.host)
    ticker = ticker.upper()
    cache_key = f"predict:{ticker}"

    cached = redis_client.get(cache_key)
    if cached:
        result = json.loads(cached)
        result["cached"] = True
        return result

    result = get_prediction(ticker)
    result["cached"] = False
    redis_client.setex(cache_key, 3600, json.dumps(result))
    return result


@app.get("/analyze/{ticker}")
def analyze(ticker: str, request: Request, question: str | None = None):
    check_rate_limit(request.client.host)
    ticker = ticker.upper()
    question = (question or f"Give me an analysis of {ticker}").strip()

    question_hash = hashlib.md5(question.lower().encode()).hexdigest()
    cache_key = f"analyze:{ticker}:{question_hash}"

	# 1. Exact match (Redis)
    cached = redis_client.get(cache_key)
    if cached:
        result = json.loads(cached)
        result["cached"] = True
        return result

	# 2. Semantic match (Qdrant) - catches reworded questions
    semantic_hit = find_similar(ticker, question)
    if semantic_hit:
        semantic_hit["cache_type"] = "semantic"
        return semantic_hit

    prediction = get_prediction(ticker)
    agent_state = agent_graph.invoke(prediction)

    result = {
        "ticker": ticker,
        "question": question,
        "last_close": prediction["last_close"],
        "rsi14": prediction["rsi14"],
        "forecast": prediction["forecast"],
        "report": agent_state["final_report"],
        "recommendation": agent_state["recommendation"],
        "cached": False,
    }
    redis_client.setex(cache_key, 3600, json.dumps(result))
    store_semantic(ticker, question, result)
    return result
