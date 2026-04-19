import sys
import os
from dotenv import load_dotenv

# Load environment variables FIRST before any other imports
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.analyze import router as analyze_router

app = FastAPI(title="AI Document Analysis API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(analyze_router)


@app.get("/")
async def root():
    return {"message": "AI Call Analytics API is running. Visit /docs for documentation."}


@app.get("/health")
async def health_check():
    return {"status": "ok"}
