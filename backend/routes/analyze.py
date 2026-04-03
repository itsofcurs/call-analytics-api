import base64
import os
import tempfile
import whisper
import time
import re
import subprocess
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, Request
from pydantic import BaseModel
from typing import List, Dict, Any

from services.stt import transcribe_audio_bytes
from services.summarizer import summarize_text
from utils.file_type import is_allowed_content_type
from utils.auth import verify_api_key

router = APIRouter(prefix="", tags=["analysis"])
ALLOWED_AUDIO_TYPES = {"audio/mpeg", "audio/wav", "audio/mp3", "audio/x-wav"}

# Load Whisper model globally - Track 3 Performance Optimization
print("Attempting to load Whisper 'base' model globally for better accuracy...")
try:
    model = whisper.load_model("base")
except Exception:
    print("Falling back to Whisper 'small' model...")
    model = whisper.load_model("small")

# BONUS: Vector DB / In-Memory Store
TRANSCRIPT_DB = []

# --- Pydantic Models for Track 3 ---
class CallAnalysisRequest(BaseModel):
    language: str
    audioFormat: str
    audioBase64: str

class SopValidation(BaseModel):
    greeting: bool
    identification: bool
    problemStatement: bool
    solutionOffering: bool
    closing: bool
    complianceScore: float
    adherenceStatus: str
    explanation: str

class AnalyticsData(BaseModel):
    paymentPreference: str
    rejectionReason: str
    sentiment: str

class CallAnalysisResponse(BaseModel):
    status: str
    language: str
    transcript: str
    summary: str
    sop_validation: SopValidation
    analytics: AnalyticsData
    keywords: List[str]

# --- Helper functions for explicit Track 3 logic ---
def extract_keywords(text: str, summary: str = "") -> List[str]:
    important = ["loan", "emi", "payment", "approval", "interest", "plan", "offer", "budget", "due", "money", "amount"]
    found = []
    lower = text.lower() + " " + summary.lower()
    for w in lower.split():
        w_clean = re.sub(r'[^a-z]', '', w)
        if w_clean in important and w_clean not in found:
            found.append(w_clean)
            if len(found) >= 10:
                break
    return found[:10]

def analyze_sentiment(text: str) -> str:
    lower = text.lower()
    pos = ["yes", "okay", "interested", "sure", "agree", "ok", "fine", "seri", "paravala"]
    neg = ["no", "can't pay", "cannot pay", "not interested", "reject", "later", "illa", "mudiyadhu"]
    pos_c = sum(1 for w in pos if w in lower)
    neg_c = sum(1 for w in neg if w in lower)
    if pos_c > neg_c:
        return "Positive"
    if neg_c > pos_c:
        return "Negative"
    return "Neutral"

def validate_sop(text: str) -> SopValidation:
    lower = text.lower()
    
    greeting = any(w in lower for w in ["hello", "hi", "namaste", "vanakkam"])
    identification = any(w in lower for w in ["i am", "calling from", "this is"])
    problemStatement = any(w in lower for w in ["loan", "payment", "due", "amount"])
    solutionOffering = any(w in lower for w in ["emi", "option", "plan", "installment"])
    closing = any(w in lower for w in ["thank you", "will call", "next step", "follow up"])
    
    checks = [greeting, identification, problemStatement, solutionOffering, closing]
    true_count = sum(1 for c in checks if c)
    complianceScore = true_count / 5.0
    adherenceStatus = "FOLLOWED" if true_count == 5 else "NOT_FOLLOWED"
    
    missing = []
    if not greeting: missing.append("greeting")
    if not identification: missing.append("identification")
    if not problemStatement: missing.append("problem statement")
    if not solutionOffering: missing.append("solution offering")
    if not closing: missing.append("closing")
    
    explanation = f"Missed steps: {', '.join(missing)}." if missing else "All SOP steps followed."
    
    return SopValidation(
        greeting=greeting,
        identification=identification,
        problemStatement=problemStatement,
        solutionOffering=solutionOffering,
        closing=closing,
        complianceScore=complianceScore,
        adherenceStatus=adherenceStatus,
        explanation=explanation
    )

def identify_payment(text: str) -> str:
    lower = text.lower()
    if "full payment" in lower or "one time" in lower:
        return "FULL_PAYMENT"
    if "part payment" in lower or "partial" in lower or "some amount" in lower:
        return "PARTIAL_PAYMENT"
    if "down payment" in lower:
        return "DOWN_PAYMENT"
    if "emi" in lower or "installment" in lower:
        return "EMI"
    return "NONE"

def identify_rejection(text: str) -> str:
    lower = text.lower()
    if any(w in lower for w in ["no money", "can't pay", "cannot pay", "budget illa"]):
        return "BUDGET_CONSTRAINTS"
    if any(w in lower for w in ["too costly", "high interest", "expensive"]):
        return "HIGH_INTEREST"
    if "already paid" in lower:
        return "ALREADY_PAID"
    if any(w in lower for w in ["not interested", "venam"]):
        return "NOT_INTERESTED"
    return "NONE"

@router.post("/analyze-document")
async def analyze_document(
    file: UploadFile = File(...),
    _: bool = Depends(verify_api_key),
):
    if not is_allowed_content_type(file.content_type):
        raise HTTPException(status_code=400, detail="Unsupported file type. Allowed: PDF, DOCX, images.")

    try:
        from services.analyzer import analyze_document_service
        analysis = await analyze_document_service(file)
        return analysis
    except HTTPException:
        raise
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail="Failed to analyze document") from exc


@router.post("/analyze-audio")
async def analyze_audio(
    file: UploadFile = File(...),
    _: bool = Depends(verify_api_key),
):
    if file.content_type not in ALLOWED_AUDIO_TYPES:
        raise HTTPException(status_code=400, detail="Unsupported audio type. Use MP3/WAV.")

    try:
        from tasks import analyze_audio_task
        audio_bytes = await file.read()
        b64_audio = base64.b64encode(audio_bytes).decode("utf-8")
        result = analyze_audio_task(b64_audio, content_type=file.content_type)
        return result
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail="Failed to queue audio analysis") from exc


@router.post("/analyze-call")
async def analyze_call(
    request: CallAnalysisRequest,
    _: bool = Depends(verify_api_key),
):
    if not request.audioBase64:
        return {"status": "error", "message": "Empty audioBase64 payload"}

    try:
        try:
            b64_string = request.audioBase64
            if "," in b64_string:
                b64_string = b64_string.split(",")[1]
            b64_string += "=" * ((4 - len(b64_string) % 4) % 4)
            audio_bytes = base64.b64decode(b64_string)
            if not audio_bytes:
                return {"status": "error", "message": "Decoded audio is empty"}
        except Exception:
            return {"status": "error", "message": "Invalid base64 encoding"}

        temp_input_path = None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{request.audioFormat}") as temp_audio:
                temp_audio.write(audio_bytes)
                temp_audio.flush()
                temp_input_path = temp_audio.name
                
            # Multilingual transcription logic
            def run_deepgram_stt():
                try:
                    import urllib.request
                    import json
                    lang = request.language.lower()
                    if lang == "tamil":
                        url = "https://api.deepgram.com/v1/listen?model=nova-3&smart_format=true&language=ta"
                    elif lang == "hindi":
                        url = "https://api.deepgram.com/v1/listen?model=nova-2&smart_format=true&language=hi"
                    else:
                        url = "https://api.deepgram.com/v1/listen?model=nova-2&smart_format=true&language=en-IN"
                    
                    req = urllib.request.Request(url, data=audio_bytes, headers={
                        "Authorization": "Token f0897d4e6b5d12ee480639476bbc6e2c2032e752",
                        "Content-Type": f"audio/{request.audioFormat}"
                    })
                    with urllib.request.urlopen(req) as response:
                        res = json.loads(response.read().decode())
                        return res["results"]["channels"][0]["alternatives"][0]["transcript"]
                except Exception as e:
                    print(f"Deepgram STT Error: {e}")
                    return ""

            def run_whisper():
                try:
                    if request.language.lower() == "tamil":
                        return model.transcribe(temp_input_path, fp16=False)
                    return model.transcribe(temp_input_path, language="en", fp16=False)
                except Exception:
                    return None
            
            final_transcript = run_deepgram_stt()
            if not final_transcript:
                print("Deepgram failed. Falling back to Whisper...")
                whisper_res = run_whisper()
                final_transcript = whisper_res["text"] if whisper_res else ""

            transcript = final_transcript.strip()
            if not transcript:
                return {"status": "error", "message": "Transcription failed"}

            # Normalization Layer
            transcript = transcript.replace("hu gaya", "has been").replace("iruku", "is available")
            
            summary = summarize_text(transcript, request.language)
            sop_validation = validate_sop(transcript)
            analytics = AnalyticsData(
                paymentPreference=identify_payment(transcript),
                rejectionReason=identify_rejection(transcript),
                sentiment=analyze_sentiment(transcript)
            )
            keywords = extract_keywords(transcript, summary)

            # Update DB for reports/recent uploads
            doc_id = len(TRANSCRIPT_DB) + 1
            new_entry = {
                "id": doc_id,
                "title": f"Call Analysis #{doc_id}",
                "status": "Ready",
                "language": request.language,
                "transcript": transcript,
                "summary": summary,
                "sentiment": analytics.sentiment,
                "sop_score": sop_validation.complianceScore,
                "timestamp": time.time()
            }
            TRANSCRIPT_DB.append(new_entry)

            return CallAnalysisResponse(
                status="success",
                language=request.language,
                transcript=transcript,
                summary=summary,
                sop_validation=sop_validation,
                analytics=analytics,
                keywords=keywords
            )
            
        finally:
            if temp_input_path and os.path.exists(temp_input_path):
                try: os.remove(temp_input_path)
                except: pass
                    
    except Exception as e:
        return {"status": "error", "message": f"Server error: {str(e)}"}

@router.get("/documents")
async def get_documents(_: bool = Depends(verify_api_key)):
    return TRANSCRIPT_DB

@router.get("/analysis")
async def get_analysis(_: bool = Depends(verify_api_key)):
    if not TRANSCRIPT_DB: return {}
    return TRANSCRIPT_DB[-1]

# BONUS Vector DB search endpoint
class SearchRequest(BaseModel):
    query: str

@router.post("/search-transcripts")
async def search_transcripts(
    request: SearchRequest,
    _: bool = Depends(verify_api_key),
):
    query = request.query.lower()
    results = [doc for doc in TRANSCRIPT_DB if query in doc["transcript"].lower() or query in doc["summary"].lower()]
    return results
