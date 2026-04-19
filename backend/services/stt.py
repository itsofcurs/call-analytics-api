import base64
import os
import re
import requests
from typing import Optional
from fastapi import HTTPException

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY", "")

def _clean_transcript(text: str) -> str:
    if not text: return ""
    # 1. Deduplicate repetitive words (e.g. "Coding coding coding" -> "Coding")
    cleaned = re.sub(r'\b(\w+)( \1)+\b', r'\1', text, flags=re.IGNORECASE)
    
    # 2. Phonetic normalization for key business terms
    # Fixes ASR mishearing of specialized terms
    corrections = {
        "ema": "EMI",
        "i i t": "IIT",
        "i t level": "IT level"
    }
    for wrong, right in corrections.items():
        pattern = re.compile(re.escape(wrong), re.IGNORECASE)
        cleaned = pattern.sub(right, cleaned)
        
    return cleaned.strip()


def transcribe_audio_bytes(data: bytes, language: Optional[str] = None) -> str:
    if not data:
        raise HTTPException(status_code=400, detail="Empty audio payload")

    if not DEEPGRAM_API_KEY:
        raise HTTPException(status_code=500, detail="DEEPGRAM_API_KEY not configured")

    lang_code = "en-IN"
    l_lower = (language or "").lower()
    if "tamil" in l_lower: lang_code = "ta"
    elif "hindi" in l_lower: lang_code = "hi"

    # Upgraded URL with Diarize (Speaker labels) and Redact (PII protection)
    dg_url = f"https://api.deepgram.com/v1/listen?model=nova-2&smart_format=true&language={lang_code}&diarize=true&redact=pci&redact=ssn&redact=numbers"
    
    try:
        response = requests.post(
            dg_url,
            headers={"Authorization": f"Token {DEEPGRAM_API_KEY}", "Content-Type": "audio/wav"},
            data=data,
            timeout=45
        )
        response.raise_for_status()
        result = response.json()
        
        # New: Process Diarized Result (Speaker Labels)
        words = result["results"]["channels"][0]["alternatives"][0].get("words", [])
        if not words:
            return _clean_transcript(result["results"]["channels"][0]["alternatives"][0]["transcript"])

        processed_transcript = ""
        current_speaker = -1
        
        for w in words:
            speaker = w.get("speaker", 0)
            if speaker != current_speaker:
                label = "Agent" if speaker == 0 else "Customer"
                processed_transcript += f"\n{label}: "
                current_speaker = speaker
            processed_transcript += w["word"] + " "
            
        transcript = _clean_transcript(processed_transcript)
        
    except Exception as exc:
        print(f"Deepgram Error: {exc}")
        raise HTTPException(status_code=500, detail=f"Speech-to-text failed: {str(exc)}")

    if not transcript:
        raise HTTPException(status_code=422, detail="No transcript produced")
        
    return transcript


def transcribe_base64(b64_audio: str, language: Optional[str] = None) -> str:
    try:
        # Handle data-uri prefix if present
        if "," in b64_audio:
            b64_audio = b64_audio.split(",")[1]
        audio_bytes = base64.b64decode(b64_audio)
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Invalid base64 audio encoding")
    return transcribe_audio_bytes(audio_bytes, language=language)
