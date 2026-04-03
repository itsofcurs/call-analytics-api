import re
from fastapi import HTTPException, UploadFile

from utils.text_extractor import extract_text
from services.summarizer import summarize_text
from services.sentiment import analyze_sentiment


def _extract_entities(text: str, max_entities: int = 15) -> list[str]:
    # Simple heuristic: collect capitalized words as pseudo-entities.
    candidates = re.findall(r"\b[A-Z][a-zA-Z]{2,}\b", text)
    seen = set()
    entities = []
    for token in candidates:
        if token not in seen:
            seen.add(token)
            entities.append(token)
        if len(entities) >= max_entities:
            break
    return entities


async def analyze_document_service(file: UploadFile):
    text = await extract_text(file)
    if not text:
        raise HTTPException(status_code=422, detail="Could not extract text from document.")

    summary = summarize_text(text)
    sentiment_result = analyze_sentiment(text)
    entities = _extract_entities(text)

    return {
        "summary": summary,
        "entities": entities,
        "sentiment": sentiment_result.get("sentiment", "neutral"),
    }
