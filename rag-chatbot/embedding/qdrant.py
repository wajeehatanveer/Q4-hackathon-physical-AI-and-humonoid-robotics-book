from qdrant_client import QdrantClient, models
from dotenv import load_dotenv
from pathlib import Path
import os
from types import SimpleNamespace

# Load the .env file from rag-chatbot directory
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

QDRANT_URL = os.getenv("QDRANT_URL", "")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "")

# Normalize values: remove surrounding quotes
if QDRANT_URL:
    QDRANT_URL = QDRANT_URL.strip().strip('"').strip("'")
if QDRANT_API_KEY:
    QDRANT_API_KEY = QDRANT_API_KEY.strip().strip('"').strip("'")

COLLECTION_NAME = "physical_ai_book"


def get_qdrant_client():
    """Initializes and returns a Qdrant client."""
    if not QDRANT_URL or not QDRANT_API_KEY:
        raise ValueError("QDRANT_URL and QDRANT_API_KEY must be set in environment variables.")
    
    client = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
        timeout=60.0,  # Increase timeout to 60 seconds for cloud operations
    )
    return client


def recreate_qdrant_collection(client: QdrantClient, vector_size: int = 768):
    """Recreates the Qdrant collection, deleting it if it already exists."""
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(size=vector_size, distance=models.Distance.COSINE),
    )
    print(f"Collection '{COLLECTION_NAME}' recreated with vector size {vector_size}.")


def upsert_vectors_to_qdrant(client: QdrantClient, vectors: list, payloads: list):
    """Upserts vectors and payloads to the Qdrant collection."""
    points = [
        models.PointStruct(
            id=idx,
            vector=vector,
            payload=payload
        )
        for idx, (vector, payload) in enumerate(zip(vectors, payloads))
    ]
    
    operation_info = client.upsert(
        collection_name=COLLECTION_NAME,
        wait=True,
        points=points,
    )
    print(f"Upserted {len(vectors)} vectors to Qdrant. Status: {operation_info.status}")
    return operation_info


def search_qdrant(client: QdrantClient, query_vector: list, limit: int = 5):
    """Performs a semantic search in the Qdrant collection using query_points."""
    try:
        # Use query_points with vector query (Qdrant client 1.7+)
        raw = client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            limit=limit,
            with_payload=True
        )
        
        # Normalize into list of objects with `.payload` and `.score`
        results = []
        for item in raw:
            payload = getattr(item, 'payload', {}) or {}
            score = getattr(item, 'score', 0.0) or 0.0
            results.append(SimpleNamespace(payload=payload, score=float(score)))
        
        return results
    except Exception as e:
        print(f"search_qdrant failed: {e}")
        raise RuntimeError(f"Failed to perform search on Qdrant client: {e}")
