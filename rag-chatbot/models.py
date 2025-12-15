from pydantic import BaseModel
from typing import List, Optional

class ChatRequest(BaseModel):
    query: str
    selected_text: Optional[str] = None # For "Ask AI about this text" feature

class ChatResponse(BaseModel):
    answer: str
    sources: List[str] # List of relevant MDX file names and headers
    confidence_score: float

class IngestRequest(BaseModel):
    # This model might be simple, as ingestion is often triggered internally
    # or by an admin. For now, it can be empty or have a simple trigger.
    # We can add more fields if we want to ingest specific files/paths.
    trigger: bool = True

class IngestResponse(BaseModel):
    message: str
    status: str
