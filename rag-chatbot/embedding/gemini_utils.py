import google.generativeai as genai
from dotenv import load_dotenv
from pathlib import Path
import os
import hashlib
import random
from typing import List

# Load the .env file located next to this module (rag-chatbot/.env).
# This ensures starting Uvicorn from the project root picks up the GEMINI_API_KEY
# when the key is stored in `rag-chatbot/.env`.
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Read API key but don't raise at import time. This allows the FastAPI app
# to start even when the key is not set; functions will raise when they are used.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Normalize and strip surrounding quotes/whitespace if present in .env
if GEMINI_API_KEY:
    GEMINI_API_KEY = GEMINI_API_KEY.strip().strip('"').strip("'")

GEMINI_CONFIGURED = False
if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        GEMINI_CONFIGURED = True
    except Exception as e:
        # Log warning and continue; functions will raise if called without proper config
        print(f"Warning: failed to configure Gemini API: {e}")
        GEMINI_CONFIGURED = False

def generate_embeddings(text: str) -> list:
    """Generates Gemini embeddings for the given text."""
    # Allow a local deterministic fallback when Gemini is unavailable or quota is exceeded.
    use_fallback = os.getenv("FALLBACK_EMBEDDINGS", "false").lower() in ("1", "true", "yes")

    if GEMINI_CONFIGURED and not use_fallback:
        try:
            result = genai.embed_content(
                model="models/embedding-001",
                content=text,
                task_type="retrieval_document"
            )
            return list(result['embedding'])
        except Exception as e:
            # Print the exception for debugging, then fall back to a local embedding if possible.
            print(f"Gemini embedding failed: {e}. Falling back to local deterministic embeddings.")

    # Deterministic fallback: use a hash-derived random seed so same text -> same vector.
    def _fallback_vector(s: str, dim: int = 768) -> List[float]:
        h = hashlib.sha256(s.encode('utf-8')).digest()
        seed = int.from_bytes(h[:8], "big")
        rnd = random.Random(seed)
        # Generate floats in range [-1, 1]
        return [rnd.random() * 2.0 - 1.0 for _ in range(dim)]

    return _fallback_vector(text)

def get_chat_completion(prompt: str, model: str = "gemini-2.5-flash") -> str:
    """Gets a chat completion from a Gemini model."""
    if not GEMINI_CONFIGURED:
        raise RuntimeError("GEMINI_API_KEY not set. Set the GEMINI_API_KEY environment variable before calling get_chat_completion.")
    model = genai.GenerativeModel(model)
    response = model.generate_content(prompt)
    return response.text