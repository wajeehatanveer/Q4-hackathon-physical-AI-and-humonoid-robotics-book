import os
import traceback
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
key = os.getenv("GEMINI_API_KEY")
print("GEMINI_API_KEY present:", bool(key))
print("Key (masked):", key[:10] + "..." if key else None)

if key:
    genai.configure(api_key=key)
    try:
        # Try to list models
        print("\n--- Attempting to list models ---")
        import google.ai.generativelanguage as glm
        from google.api_core import gapic_v1
        import grpc
        
        # Try direct API call if available
        try:
            from google.generativeai import types
            models_resp = genai.list_models()
            print("Available models:")
            for m in models_resp:
                print(f"  - {m.name}")
        except Exception as e:
            print("list_models() failed:", type(e).__name__, str(e)[:200])
        
        # Try a simple embed call to test quota
        print("\n--- Testing embed_content (quota check) ---")
        try:
            result = genai.embed_content(
                model="models/embedding-001",
                content="test",
                task_type="retrieval_document"
            )
            print("✓ embed_content succeeded")
        except Exception as e:
            print(f"✗ embed_content failed: {type(e).__name__}")
            print(f"  Message: {str(e)[:300]}")
    
    except Exception as e:
        print("Error during Gemini checks:")
        traceback.print_exc()
else:
    print("ERROR: GEMINI_API_KEY not found in .env")
