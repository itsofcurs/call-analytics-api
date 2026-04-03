import re
from collections import Counter
from typing import Dict, List

REJECTION_PATTERNS = {
    "price": [r"too expensive", r"cost too high", r"price issue"],
    "timing": [r"call later", r"busy", r"not now"],
    "trust": [r"dont trust", r"scam", r"fraud"],
    "need": [r"dont need", r"not interested", r"no need"],
}


def analyze_rejections(text: str) -> dict:
    lower = text.lower()
    reasons: List[str] = []
    counts: Counter = Counter()

    for category, patterns in REJECTION_PATTERNS.items():
        for pat in patterns:
            for match in re.finditer(pat, lower, flags=re.IGNORECASE):
                reasons.append(match.group(0))
                counts[category] += 1

    return {
        "reasons": reasons,
        "categories": {cat: counts.get(cat, 0) for cat in REJECTION_PATTERNS.keys()},
    }
