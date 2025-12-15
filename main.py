import sys
from pathlib import Path

# Add rag-chatbot to path
sys.path.insert(0, str(Path(__file__).parent / "rag-chatbot"))

# Remove main from modules to avoid circular import
for key in list(sys.modules.keys()):
    if "main" in key and "rag_chatbot" not in key:
        del sys.modules[key]

# Load rag-chatbot/main.py using spec
import importlib.util
spec = importlib.util.spec_from_file_location("rag_chatbot_main", str(Path(__file__).parent / "rag-chatbot" / "main.py"))
rag_module = importlib.util.module_from_spec(spec)
sys.modules["rag_chatbot_main"] = rag_module
spec.loader.exec_module(rag_module)

app = rag_module.app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
