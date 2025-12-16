#!/usr/bin/env python3
from pathlib import Path
from dotenv import load_dotenv
import os

# Load from rag-chatbot/.env
rag_dir = Path(__file__).parent / "rag-chatbot"
env_path = rag_dir / ".env"

print(f"Loading .env from: {env_path}")
print(f"Exists: {env_path.exists()}")

load_dotenv(dotenv_path=env_path)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

print(f"\nGEMINI_API_KEY: {'SET' if GEMINI_API_KEY else 'NOT SET'}")
print(f"QDRANT_URL: {QDRANT_URL[:50] if QDRANT_URL else 'NOT SET'}...")
print(f"QDRANT_API_KEY: {'SET' if QDRANT_API_KEY else 'NOT SET'}")

# Now test imports
try:
    from rag_chatbot.embedding.qdrant import get_qdrant_client
    print("\n✓ Successfully imported get_qdrant_client")
    
    # Try to get the client
    client = get_qdrant_client()
    print("✓ Successfully created Qdrant client")
except Exception as e:
    print(f"\n✗ Error: {e}")
