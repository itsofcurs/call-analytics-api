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
    sentences = [s.strip() for s in re.split(r'[.!?]+', text) if len(s.strip()) > 5]
    if not sentences:
        return "Agent and customer discussed the call details."
    
    # Take the first and maybe a middle/last sentence
    best_summary = sentences[0].capitalize() + "."
    if len(sentences) > 1:
        best_summary += " " + sentences[-1].capitalize() + "."
    
    return best_summary
