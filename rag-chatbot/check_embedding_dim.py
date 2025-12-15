from embedding.gemini_utils import generate_embeddings
import google.generativeai as genai
emb = generate_embeddings("test")
print("Embedding dimension:", len(emb))
print("Current model in generate_embeddings: models/gemini-embedding-001")
print("\nAvailable embedding models:")
models_list = genai.list_models()
embed_models = [m for m in models_list if 'embed' in m.name.lower()]
for m in embed_models:
    print(f"  {m.name}")
