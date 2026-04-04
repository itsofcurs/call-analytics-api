import sys
import os
# Add the current directory (backend) to the Python path so sub-packages work correctly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

from routes.analyze import router as analyze_router

load_dotenv()

app = FastAPI(title="AI Document Analysis API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(analyze_router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
