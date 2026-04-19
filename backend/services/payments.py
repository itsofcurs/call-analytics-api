import re
from collections import Counter
from typing import Dict, List

PAYMENT_PATTERNS = {
    "emi": [r"\bemi\b", r"\bema\b", r"installment", r"monthly payment"],
    "full": [r"full payment", r"paid in full", r"one time"],
    "partial": [r"partial payment", r"part payment", r"advance"],
    "down": [r"down payment", r"token amount", r"booking amount"],
}


def categorize_payments(text: str) -> dict:
    lower = text.lower()
    mentions: List[str] = []
    counts: Counter = Counter()

    for category, patterns in PAYMENT_PATTERNS.items():
        for pat in patterns:
            for match in re.finditer(pat, lower, flags=re.IGNORECASE):
                mentions.append(match.group(0))
                counts[category] += 1

    return {
        "counts": {
            "emi": counts.get("emi", 0),
            "full": counts.get("full", 0),
            "partial": counts.get("partial", 0),
            "down": counts.get("down", 0),
        },
        "mentions": mentions,
    }
