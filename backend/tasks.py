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
    summary = summarize_text(transcript)
    sentiment = analyze_sentiment(transcript).get("sentiment", "neutral")
    sop = evaluate_sop(transcript)
    payments = categorize_payments(transcript)
    rejections = analyze_rejections(transcript)
    entities = _extract_entities(transcript)

    return {
        "transcript": transcript,
        "summary": summary,
        "sentiment": sentiment,
        "sop": sop,
        "payments": payments,
        "rejections": rejections,
        "entities": entities,
    }
