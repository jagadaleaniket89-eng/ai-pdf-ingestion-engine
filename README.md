# AI PDF Ingestion Engine

Upload a PDF (up to 50MB) and get a short or detailed AI analysis.
Built with FastAPI + Gemini 2.5 Flash. No vector database required.

🔗 **Live demo:** <https://ai-pdf-ingestion-engine.onrender.com/>  (free tier: first load may take ~30s)

## Why no vector DB?
Gemini 2.5 Flash has a long context window and reads PDFs natively
(text, tables, images). For single-document Q&A and summaries, this
avoids chunking, embedding costs, and extra infrastructure.
Trade-off: not suited for searching across thousands of documents.

## Features
- Short and detailed analysis modes
- Handles PDFs up to 50MB
- Password-protected endpoints to prevent API quota abuse
- Concurrent multi-client requests
- CORS configured for the frontend

## Architecture
Browser → FastAPI (/analyze) → temp file → Gemini API → response

## Tech stack
FastAPI, Google GenAI SDK, HTML5, Render, python-dotenv

## Run locally
git clone ...
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add GEMINI_API_KEY and APP_PASSWORD
uvicorn main:app --reload

## API
POST /analyze  (multipart: file, mode, password) → JSON

## Challenges & what I learned
- (e.g., handling large uploads without blowing memory)
- (e.g., protecting a free API key on a public URL)

## Limitations & future work
- Single-document only, no persistence
- Add rate limiting, proper auth, tests, Docker


