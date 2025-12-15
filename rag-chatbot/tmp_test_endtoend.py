import traceback
from embedding.gemini_utils import generate_embeddings
from embedding.qdrant import get_qdrant_client, search_qdrant

try:
    vec = generate_embeddings('What is humanoid robotics?')
    print('Generated embedding length=', len(vec))
    client = get_qdrant_client()
    res = search_qdrant(client, vec, limit=3)
    print('Search returned', len(res))
    for r in res:
        print('score=', r.score, 'keys=', list(r.payload.keys())[:5])
except Exception as e:
    print('Error:')
    traceback.print_exc()
