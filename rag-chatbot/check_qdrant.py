from embedding.qdrant import get_qdrant_client, COLLECTION_NAME

client = get_qdrant_client()
try:
    collection_info = client.get_collection(COLLECTION_NAME)
    print(f"Collection '{COLLECTION_NAME}':")
    print(f"  Points count: {collection_info.points_count}")
    print(f"  Status: {collection_info.status}")
    
    if collection_info.points_count == 0:
        print("\n⚠️  Collection is EMPTY! Need to run /ingest first.")
    else:
        print(f"\n✓ Collection has {collection_info.points_count} vectors ready.")
except Exception as e:
    print(f"Error: {e}")
