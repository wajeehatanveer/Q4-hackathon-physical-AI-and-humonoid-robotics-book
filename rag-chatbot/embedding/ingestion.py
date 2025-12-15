import os
import glob
from typing import List, Dict
from pathlib import Path
from dotenv import load_dotenv
from .qdrant import get_qdrant_client, recreate_qdrant_collection, upsert_vectors_to_qdrant
from .gemini_utils import generate_embeddings
import re

# Load the .env file from rag-chatbot directory to ensure all env vars are available
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

def get_mdx_files(directory: str) -> List[str]:
    """Finds all .mdx files in a directory."""
    return glob.glob(os.path.join(directory, "**", "*.mdx"), recursive=True)

def extract_frontmatter_and_content(file_path: str) -> (Dict, str):
    """Extracts frontmatter and content from an MDX file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    frontmatter = {}
    match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if match:
        frontmatter_str = match.group(1)
        for line in frontmatter_str.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                frontmatter[key.strip()] = value.strip()
        # Remove frontmatter from content
        content = content[match.end():]
    return frontmatter, content

def process_and_embed_files(file_paths: List[str]):
    """Processes, chunks, and embeds .mdx files, then upserts them to Qdrant."""
    qdrant_client = get_qdrant_client()
    # Gemini's embedding-001 model has a dimension of 768.
    recreate_qdrant_collection(qdrant_client, vector_size=768)

    all_vectors = []
    all_payloads = []

    for file_path in file_paths:
        frontmatter, content = extract_frontmatter_and_content(file_path)
        # For simplicity, sending the entire content as one chunk for now.
        # A more sophisticated chunking strategy can be implemented here if needed.
        chunk = content 

        embedding = generate_embeddings(chunk)
        all_vectors.append(embedding)

        payload = {
            "source": file_path,
            "chunk_index": 0, # Since we're not chunking, index is always 0
            "text": chunk,
            "title": frontmatter.get('title', os.path.basename(file_path)),
        }
        all_payloads.append(payload)

        # To avoid hitting rate limits and to manage memory, upsert in batches
        if len(all_vectors) >= 50:
            upsert_vectors_to_qdrant(qdrant_client, all_vectors, all_payloads)
            all_vectors, all_payloads = [], []

    # Upsert any remaining vectors
    if all_vectors:
        upsert_vectors_to_qdrant(qdrant_client, all_vectors, all_payloads)

if __name__ == "__main__":
    # This part is for running the ingestion script directly
    # The path should be relative to the root of the docusaurus project
    mdx_files = get_mdx_files("../docs") # Go up one level from rag-chatbot to physical-AI-book
    process_and_embed_files(mdx_files)
    print("Ingestion complete.")
