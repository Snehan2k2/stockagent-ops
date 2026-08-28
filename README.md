# build-stock-agent-ops

A small MLOps pipeline for stock analysis. Fetches real stock data, computes technical indicators, generates a forecast (no ML training — a deterministic formula), and uses local AI agents to write a report. A learning project, not for real trading decisions.

## Prerequisites

- Docker Desktop, running
- [Ollama](https://ollama.com) installed — open the Ollama app (menu bar icon confirms it's running), then pull the models:
  ```bash
  ollama pull qwen3.5:2b
  ollama pull nomic-embed-text
  ```

## Run it

First time, or after changing any code:
```bash
docker-compose up --build
```

Already built before, just starting it again:
```bash
docker-compose up
```
Reuses the existing images — no rebuild, starts in seconds.

Starts 5 services: Redis (caching), Qdrant (semantic caching), Prometheus (metrics), the FastAPI backend, and the Streamlit frontend. First run takes a few minutes to build the images.

## Test it

**Frontend (easiest):** open `http://localhost:8501`. Enter a ticker (e.g. `AAPL`), optionally a question, click Analyze.

**API directly:**
```bash
curl http://localhost:8000/health
curl http://localhost:8000/predict/AAPL
curl "http://localhost:8000/analyze/AAPL?question=should%20I%20buy%20right%20now"
```

**Metrics:** `http://localhost:9090/targets` — should show the backend target as "up".

## Notes

- Only `AAPL` has data by default. To add another ticker, run `uv run main.py` on the host first (edit `DEFAULT_TICKER` in `src/config.py`) — the API only reads from `feature_store/data/features.parquet`, it doesn't fetch new tickers on its own.
- Stop everything: `docker-compose stop` (keeps cached data) or `docker-compose down` (removes containers, wipes Redis/Qdrant's in-container data).
