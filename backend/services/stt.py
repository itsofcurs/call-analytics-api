import base64
import os
import tempfile
from typing import Any, Optional

from fastapi import HTTPException

DEFAULT_MODEL = os.getenv("WHISPER_MODEL", "small")
COMPUTE_TYPE = os.getenv("WHISPER_COMPUTE_TYPE", "int8")

# Lazy load model
_model: Optional[Any] = None


def _get_model() -> Any:
    global _model
    if _model is None:
        try:
            from faster_whisper import WhisperModel

            _model = WhisperModel(DEFAULT_MODEL, compute_type=COMPUTE_TYPE)
        except ModuleNotFoundError as exc:  # pragma: no cover
            raise HTTPException(status_code=500, detail="STT dependency missing: install faster-whisper") from exc
        except Exception as exc:  # pragma: no cover
            raise HTTPException(status_code=500, detail="Failed to load STT model") from exc
    return _model


def transcribe_audio_bytes(data: bytes, language: Optional[str] = None) -> str:
    if not data:
        raise HTTPException(status_code=400, detail="Empty audio payload")

    model = _get_model()

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as tmp:
        tmp.write(data)
        tmp.flush()
        try:
            segments, _ = model.transcribe(
                tmp.name,
                language=language,  # None lets model auto-detect; supports Hindi/Tamil
                beam_size=5,
                vad_filter=True,
            )
            transcript = " ".join([seg.text.strip() for seg in segments]).strip()
        except Exception as exc:  # pragma: no cover
            raise HTTPException(status_code=500, detail="Speech-to-text failed") from exc

    if not transcript:
        raise HTTPException(status_code=422, detail="No transcript produced")
    return transcript


def transcribe_base64(b64_audio: str, language: Optional[str] = None) -> str:
    try:
        audio_bytes = base64.b64decode(b64_audio)
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=400, detail="Invalid base64 audio") from exc
    return transcribe_audio_bytes(audio_bytes, language=language)
