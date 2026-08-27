import uuid

import requests
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    FieldCondition,
    Filter,
    MatchValue,
    PointStruct,
    VectorParams,
)

COLLECTION = "analysis_cache"
SIMILARITY_THRESHOLD = 0.95
EMBED_DIM = 768

qdrant = QdrantClient(host="localhost", port=6333)


def _ensure_collection():
    existing = [c.name for c in qdrant.get_collections().collections]
    if COLLECTION not in existing:
        qdrant.create_collection(
            collection_name=COLLECTION,
            vectors_config=VectorParams(size=EMBED_DIM, distance=Distance.COSINE),
        )


def embed(text: str) -> list[float]:
    resp = requests.post(
        "http://localhost:11434/api/embeddings",
        json={"model": "nomic-embed-text", "prompt": text},
    )
    return resp.json()["embedding"]


def find_similar(ticker: str, question: str) -> dict | None:
    _ensure_collection()
    vector = embed(question)
    hits = qdrant.query_points(
        collection_name=COLLECTION,
        query=vector,
        query_filter=Filter(must=[FieldCondition(key="ticker", match=MatchValue(value=ticker))]),
        limit=1,
    ).points

    if hits and hits[0].score >= SIMILARITY_THRESHOLD:
        return hits[0].payload
    return None


def store(ticker: str, question: str, result: dict):
    _ensure_collection()
    vector = embed(question)
    qdrant.upsert(
        collection_name=COLLECTION,
        points=[
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={"ticker": ticker, "question": question, **result},
            )
        ],
    )
