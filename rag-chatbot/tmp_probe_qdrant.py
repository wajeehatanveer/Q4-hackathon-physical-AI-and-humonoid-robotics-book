from embedding.qdrant import get_qdrant_client
c = get_qdrant_client()
print('Client class:', type(c))
names = [n for n in dir(c) if ('search' in n.lower() or 'point' in n.lower() or 'scroll' in n.lower() or 'query' in n.lower())]
print('\nCandidate methods (filtered):')
for n in names:
    print(' -', n)
for check in ('search','search_points','search_collection','search_batch','scroll','search_points_collection'):
    print(check, hasattr(c, check))
print('\nDone')
