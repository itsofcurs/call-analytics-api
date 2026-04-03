from functools import lru_cache

from fastapi import HTTPException
from transformers import pipeline

MODEL_NAME = "distilbert-base-uncased-finetuned-sst-2-english"
NEUTRAL_THRESHOLD = 0.55  # scores below this are treated as neutral


@lru_cache(maxsize=1)
def _get_sentiment_pipeline():
    try:
        return pipeline("sentiment-analysis", model=MODEL_NAME, tokenizer=MODEL_NAME, framework="pt")
    except Exception as exc:  # pragma: no cover - model load failures
        raise HTTPException(status_code=500, detail="Failed to load sentiment model") from exc


def analyze_sentiment(text: str) -> dict:
    if not text or not text.strip():
        raise HTTPException(status_code=400, detail="No text provided for sentiment analysis.")

    classifier = _get_sentiment_pipeline()

    try:
        outputs = classifier(text)
    except Exception as exc:  # pragma: no cover - runtime guard
        raise HTTPException(status_code=500, detail="Sentiment analysis failed.") from exc

    if not outputs:
        raise HTTPException(status_code=500, detail="Sentiment analysis returned no result.")

    result = outputs[0]
    label = result.get("label", "").lower()
    score = float(result.get("score", 0.0))

    if score < NEUTRAL_THRESHOLD:
        sentiment = "neutral"
    elif "pos" in label:
        sentiment = "positive"
    elif "neg" in label:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    return {"sentiment": sentiment, "score": score}
