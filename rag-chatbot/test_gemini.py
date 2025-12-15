import traceback
from pathlib import Path
import os

# Ensure we load rag-chatbot .env
env_path = Path(__file__).parent / '.env'
print(f"Loading env: {env_path}, exists={env_path.exists()}")

from embedding.gemini_utils import generate_embeddings, GEMINI_CONFIGURED, GEMINI_API_KEY
print('GEMINI_CONFIGURED=', GEMINI_CONFIGURED)
print('GEMINI_API_KEY present=', bool(GEMINI_API_KEY))

try:
    print('Calling generate_embeddings with short test text...')
    emb = generate_embeddings('test')
    print('Embedding length:', len(emb))
except Exception as e:
    print('Exception caught:')
    traceback.print_exc()
