import json
import os
from dataclasses import dataclass
from typing import List, Tuple

from fastapi import HTTPException

SOP_PATH = os.getenv("SOP_TEMPLATE_PATH", os.path.join(os.path.dirname(__file__), "../config/sop_templates.json"))


def _load_templates():
    try:
        with open(SOP_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="SOP template missing")
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail="Failed to load SOP template") from exc


def evaluate_sop(text: str, sop_name: str = "default") -> dict:
    templates = _load_templates()
    sop = templates.get(sop_name) or templates.get("default")
    if not sop:
        raise HTTPException(status_code=500, detail="SOP template not configured")

    lower_text = text.lower()
    required: List[str] = sop.get("required_phrases", [])
    min_score = sop.get("min_score", 0.7)

    found = []
    missing = []
    positions: List[Tuple[int, str]] = []
    for phrase in required:
        phrase_l = phrase.lower()
        idx = lower_text.find(phrase_l)
        if idx != -1:
            found.append(phrase)
            positions.append((idx, phrase))
        else:
            missing.append(phrase)

    coverage = len(found) / len(required) if required else 1.0
    ordered = sorted(positions, key=lambda x: x[0])
    in_order = [p for _, p in ordered] == found if found else True
    score = coverage * (1.0 if in_order else 0.9)

    passed = score >= min_score

    return {
        "passed": passed,
        "score": round(score, 3),
        "missing": missing,
        "found": found,
    }
