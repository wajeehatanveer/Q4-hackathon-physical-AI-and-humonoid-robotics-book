import traceback
from embedding.qdrant import get_qdrant_client, search_qdrant

client = get_qdrant_client()
vec = [0.0]*768
try:
    print('Calling search_qdrant...')
    res = search_qdrant(client, vec, limit=3)
    print('Search returned', len(res))
    for r in res:
        print('score=', r.score, 'payload keys=', list(r.payload.keys())[:5])
except Exception as e:
    print('Exception during search_qdrant:')
    traceback.print_exc()
