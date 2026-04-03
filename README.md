# Ethereal AI Document Analysis Dashboard

A full-stack AI-powered document analysis system combining a Vite/React/Tailwind dashboard with a FastAPI backend that performs text extraction (PDF/DOCX/image OCR), summarization, sentiment, and entity extraction.

## Architecture
```mermaid
graph TD
  A[React + Tailwind UI] -->|Axios / Authorization header| B[FastAPI /analyze-document]
  B --> C[Text Extraction\nPDFMiner / python-docx / Tesseract]
  B --> D[Summarization\nBART (facebook/bart-large-cnn)]
  B --> E[Sentiment\nDistilBERT SST-2]
  B --> F[Heuristic Entities]
  C --> G[(Response)]
  D --> G
  E --> G
  F --> G
```

## Setup
### Frontend
1) `cd` into project root
2) Install deps: `npm install`
3) Run dev server: `npm run dev`
4) Env vars (create `.env.local`):
   - `VITE_API_KEY=hackathon123`
   - `VITE_API_URL=http://localhost:8000`

### Backend (Python 3.11 venv recommended)
1) `cd backend`
2) Create venv: `py -3.11 -m venv .venv311`
3) Activate: `\.venv311\Scripts\activate`
4) Install deps: `pip install -r requirements.txt`
5) Set env (e.g., `.env`): `API_KEY=hackathon123`
6) Run: `uvicorn main:app --reload --host 0.0.0.0 --port 8000`

### Docker (backend)
- Build: `docker build -t ethereal-backend .`
- Run: `docker run -p 8000:8000 -e API_KEY=hackathon123 ethereal-backend`

## API
`POST /analyze-document`
- Headers: `Authorization: <API_KEY>` (or `Bearer <API_KEY>`)
- Body: `multipart/form-data` with `file` (PDF, DOCX, jpg/jpeg/png)
- Response:
```json
{
  "summary": "...",
  "entities": ["Acme", "London", ...],
  "sentiment": "positive"
}
```

## Tech Stack
- Frontend: React 18, Vite, Tailwind CSS
- Backend: FastAPI, Uvicorn
- AI/NLP: Transformers (BART for summarization, DistilBERT SST-2 for sentiment)
- Extraction: pdfminer.six, python-docx, Tesseract OCR (pytesseract/Pillow)
- Infra: Dockerfile for container deploy

## AI Tools Used
- Summarization: `facebook/bart-large-cnn`
- Sentiment: `distilbert-base-uncased-finetuned-sst-2-english`
- OCR: Tesseract

## Known Limitations
- Large models (BART/torch) increase cold start and memory usage; consider smaller models for constrained environments.
- OCR quality depends on image clarity; complex PDFs may need more robust parsing.
- Entity extraction is heuristic (capitalized tokens); replace with a proper NER model for production.
- Ensure Tesseract is installed in deployed environments or baked into the image.
