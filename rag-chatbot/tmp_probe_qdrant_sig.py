from embedding.qdrant import get_qdrant_client
import inspect
c = get_qdrant_client()
print('Client class:', type(c))

candidates = ['query_points','query','query_batch','query_points_groups','search','search_points','search_collection','search_batch','scroll']
for name in candidates:
    print('\n---', name, '---')
    if hasattr(c, name):
        obj = getattr(c, name)
        try:
            print('callable:', callable(obj))
            print('repr:', repr(obj))
            try:
                sig = inspect.signature(obj)
                print('signature:', sig)
            except Exception as e:
                print('signature error:', e)
            src = None
        except Exception as e:
            print('error introspecting:', e)
    else:
        print('NOT PRESENT')
print('\nDone')
