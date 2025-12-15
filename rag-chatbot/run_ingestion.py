# This script is a command-line utility to trigger the ingestion process.
import os
import sys

# Add the parent directory to the Python path to allow for relative imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from embedding.ingestion import get_mdx_files, process_and_embed_files

def run_ingestion():
    """
    Triggers the ingestion and embedding of all .mdx files.
    """
    try:
        # The path to the docs directory, relative to this script.
        # It needs to go up from rag-chatbot/ to the root of physical-AI-book/
        # and then into 'docs'.
        docs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'docs'))
        
        if not os.path.isdir(docs_path):
            print(f"Error: Directory not found at '{docs_path}'")
            return
            
        mdx_files = get_mdx_files(docs_path)
        if not mdx_files:
            print("No .mdx files found to ingest.")
            return
            
        print(f"Found {len(mdx_files)} MDX files to process.")
        process_and_embed_files(mdx_files)
        print("Ingestion process completed successfully.")
        
    except Exception as e:
        print(f"An error occurred during ingestion: {e}")

if __name__ == "__main__":
    print("Starting the ingestion process...")
    run_ingestion()
