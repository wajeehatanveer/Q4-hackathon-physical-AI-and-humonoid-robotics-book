# RAG Chatbot Backend for Physical AI Book

This directory contains the backend for the RAG (Retrieval-Augmented Generation) chatbot for the Physical AI Book.

## Environment Variables

Create a `.env` file in this directory with the following variables:

```
# Firebase Service Account Key
# If running locally, this should be the path to your Firebase service account JSON file.
# Example: FIREBASE_SERVICE_ACCOUNT_KEY=/app/path/to/your-service-account-key.json
# If deploying to Google Cloud, leave this unset and set GOOGLE_APPLICATION_CREDENTIALS in your environment.
FIREBASE_SERVICE_ACCOUNT_KEY=

# OpenAI API Key
OPENAI_API_KEY=

# Qdrant Cloud Configuration
QDRANT_URL=
QDRANT_API_KEY=

# Neon Serverless Postgres Configuration
DATABASE_URL=
```

## Ingestion Instructions

To ingest the content of the book into the Qdrant vector database, run the following command from this directory:

```bash
python run_ingestion.py
```

This will:
1. Find all `.mdx` files in the `docs` directory.
2. Chunk the content of each file.
3. Generate embeddings for each chunk using OpenAI's `text-embedding-3-large` model.
4. Upsert the embeddings and metadata to your Qdrant collection.

## Execution Commands

To run the backend server locally, use the following command:

```bash
uvicorn main:app --reload
```

The server will be available at `http://localhost:8000`.

## Deployment Commands

### Backend (Render / Railway)

1.  **Create a new web service** on your chosen platform (Render, Railway, etc.).
2.  **Connect your Git repository.**
3.  **Set the build command:** `pip install -r requirements.txt`
4.  **Set the start command:** `uvicorn main:app --host 0.0.0.0 --port 8000`
5.  **Add the environment variables** from your `.env` file to the platform's secret management.

### Frontend (Docusaurus)

The frontend is a static Docusaurus site and does not require any changes to its deployment process. Simply build the site and deploy the `build` directory to your hosting provider.

```bash
npm run build
```

## API Endpoints

- `GET /`: Root endpoint.
- `POST /ingest`: Protected endpoint to trigger the ingestion process.
- `POST /chat`: Protected endpoint to chat with the RAG model.
- `GET /history`: Protected endpoint to retrieve the chat history for the authenticated user.
- `GET /protected`: A sample protected endpoint.
