from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from embedding.ingestion import get_mdx_files, process_and_embed_files
from embedding.qdrant import get_qdrant_client, search_qdrant
from embedding.gemini_utils import generate_embeddings, get_chat_completion
from models import IngestResponse, ChatRequest, ChatResponse

app = FastAPI()

# Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Physical AI Book RAG Chatbot Backend!"}

@app.post("/ingest", response_model=IngestResponse)
async def ingest_data():
    """
    Public endpoint to trigger the ingestion and embedding of all .mdx files.
    """
    try:
        docs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'docs'))
        print(f"[INGEST] Looking for MDX files in: {docs_path}")
        
        if not os.path.isdir(docs_path):
            raise HTTPException(status_code=404, detail=f"Directory not found: {docs_path}")
            
        mdx_files = get_mdx_files(docs_path)
        print(f"[INGEST] Found {len(mdx_files)} MDX files")
        
        if not mdx_files:
            raise HTTPException(status_code=404, detail="No .mdx files found to ingest.")
        
        print(f"[INGEST] Starting embedding process...")    
        process_and_embed_files(mdx_files)
        
        print(f"[INGEST] Successfully ingested and embedded {len(mdx_files)} files")
        return {"message": f"Successfully ingested and embedded {len(mdx_files)} MDX files.", "status": "success"}
    except Exception as e:
        import traceback
        error_msg = f"Ingestion failed: {str(e)}\n{traceback.format_exc()}"
        print(f"[INGEST ERROR] {error_msg}", flush=True)
        import sys
        print(error_msg, file=sys.stderr, flush=True)
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")

@app.post("/chat", response_model=ChatResponse)
async def chat_with_rag(request: ChatRequest):
    """
    Main endpoint for the RAG chatbot.
    """
    try:
        import traceback
        import sys
        
        # 1. Generate embedding for the query
        query_text = request.query
        if request.selected_text:
            query_text = f"Context: {request.selected_text}\n\nQuestion: {request.query}"

        query_embedding = generate_embeddings(query_text)

        # 2. Semantic search in Qdrant
        qdrant_client = get_qdrant_client()
        search_results = search_qdrant(qdrant_client, query_embedding, limit=3)
        
        context = ""
        sources = []
        for result in search_results:
            context += result.payload.get('text', '') + "\n\n"
            title = result.payload.get('title', 'Unknown')
            source = result.payload.get('source', 'Unknown')
            sources.append(f"{title} (source: {os.path.basename(source)})")

        # 3. Construct prompt for Gemini
        prompt = f"Based on the following context from the book, answer the user's question.\n\nContext:\n{context}\n\nQuestion: {request.query}\n\nAnswer:"

        # 4. Get answer from Gemini (try) — fallback to a local responder on failure
        try:
            answer = get_chat_completion(prompt)
        except Exception as e:
            # Log the Gemini error and synthesize a fallback answer from retrieved context.
            import traceback
            tb = traceback.format_exc()
            print(f"Gemini chat failed, falling back to local responder: {e}\n{tb}", flush=True)

            # Simple fallback: use the most relevant pieces of context to construct an answer.
            if context.strip():
                # Take up to first 3 context segments (split by double newlines) to build an answer.
                parts = [p.strip() for p in context.split('\n\n') if p.strip()]
                top_parts = parts[:3]
                summary = ' '.join(top_parts)
                # Form a helpful response: restate the question, provide extracted context, and a short answer.
                answer = (
                    f"Based on the book content I found, here are the relevant excerpts:\n\n{summary}\n\n"
                    f"Answer (best-effort): I didn't reach the external chat model due to an API issue, but based on the excerpts above, my best answer is: "
                    f"{request.query} -> See the excerpts for details."
                )
            else:
                answer = (
                    "I couldn't reach the external chat model and found no relevant context in the book. "
                    "Please try again later or enable fallback embeddings." 
                )

        return ChatResponse(
            answer=answer,
            sources=list(set(sources)) if sources else ["No sources found"],
            confidence_score=search_results[0].score if search_results else 0.0
        )
    except Exception as e:
        import traceback
        error_msg = f"Chat processing failed: {str(e)}\n{traceback.format_exc()}"
        print(error_msg, file=sys.stderr)
        raise HTTPException(status_code=500, detail=f"Chat processing failed: {str(e)}")

