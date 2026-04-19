import base64
import os

from services.analyzer import _extract_entities
from services.sentiment import analyze_sentiment
from services.summarizer import summarize_text
from services.stt import transcribe_base64
from services.sop import evaluate_sop
from services.payments import categorize_payments
from services.rejections import analyze_rejections


def analyze_audio_task(b64_audio: str, content_type: str = None, language: str = None):
    transcript = transcribe_base64(b64_audio, language=language)
    from services.llm import analyze_call_with_llm
    
    # Advanced LLM Analysis
    llm_results = analyze_call_with_llm(transcript)
    
    # Extract from LLM (Aligning with Gemini 3.1 Prompt)
    summary = llm_results.get("summary", "Summary Generation Failed")
    
    # The LLM now returns these directly as per systemic prompt
    sop_val = llm_results.get("sop_validation", {})
    analytics = llm_results.get("analytics", {})
    
    # Map back to legacy keys for Postman support
    sop = {
        "score": sop_val.get("complianceScore", 0.0),
        "passed": sop_val.get("adherenceStatus") == "FOLLOWED",
        "explanation": sop_val.get("explanation", ""),
        "greeting": sop_val.get("greeting", False),
        "identification": sop_val.get("identification", False),
        "problemStatement": sop_val.get("problemStatement", False),
        "solutionOffering": sop_val.get("solutionOffering", False),
        "closing": sop_val.get("closing", False)
    }
    
    payments = {
        "preference": analytics.get("paymentPreference", "NONE"),
        "reason": analytics.get("rejectionReason", "NONE")
    }
    
    rejections = {
        "category": analytics.get("rejectionReason", "NONE")
    }
    
    sentiment = analytics.get("sentiment", analyze_sentiment(transcript).get("sentiment", "neutral"))
    entities = _extract_entities(transcript)

    return {
        "transcript": transcript,
        "summary": summary,
        "sentiment": sentiment,
        "sop": sop, # Legacy
        "sop_validation": sop_val, # Rubric
        "payments": payments, # Legacy
        "rejections": rejections, # Legacy
        "analytics": analytics, # Rubric
        "entities": entities,
        "keywords": llm_results.get("keywords") or entities
    }
