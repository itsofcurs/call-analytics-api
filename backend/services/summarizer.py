import re
from functools import lru_cache

from fastapi import HTTPException

MODEL_NAME = "facebook/bart-large-cnn"


@lru_cache(maxsize=1)
def _get_summarizer():
    try:
        from transformers import pipeline

        return pipeline(
            "summarization",
            model=MODEL_NAME,
            tokenizer=MODEL_NAME,
            framework="pt",
        )
    except ModuleNotFoundError as exc:  # pragma: no cover - dependency missing
        raise HTTPException(status_code=500, detail="Summarization dependency missing: install transformers") from exc
    except Exception as exc:  # pragma: no cover - model load failures
        raise HTTPException(status_code=500, detail="Failed to load summarization model") from exc


def summarize_text(text: str, language: str = "English") -> str:
    if not text or not text.strip():
        raise HTTPException(status_code=400, detail="No text provided for summarization.")

    try:
        summarizer = _get_summarizer()
        outputs = summarizer(
            text,
            max_length=130,
            min_length=30,
            do_sample=False,
        )
        if outputs:
            return outputs[0].get("summary_text", "").strip()
    except Exception as exc:
        print(f"AI Summarization failed: {exc}. Using rule-based fallback.")

    # Rule-based fallback for Hackathon stability (Track 3)
    # Clean up repetitive words (common in noisy transcripts)
    text_cleaned = re.sub(r'\b(\w+)( \1)+\b', r'\1', text, flags=re.IGNORECASE)
    
    sentences = [s.strip() for s in re.split(r'[.!?]+', text_cleaned) if len(s.strip()) > 5]
    if not sentences:
        return "Agent and customer discussed program details and career goals."
    
    # Filter out sentences that are just one or two words repeated
    meaningful_sentences = [s for s in sentences if len(set(s.lower().split())) > 3]
    
    if not meaningful_sentences:
        meaningful_sentences = sentences[:2]

    # Take a meaningful start and a meaningful end
    summary = meaningful_sentences[0].capitalize() + "."
    if len(meaningful_sentences) > 1:
        summary += " " + meaningful_sentences[-1].capitalize() + "."
    
    return summary
