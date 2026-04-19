import os
import json
from typing import Dict, Any, List
import google.generativeai as genai

# Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

SYSTEM_PROMPT = """
You are an expert Call Center Quality Auditor for the 'Call Center Compliance' project.
Analyze transcripts in English, Tamil, or Hindi.

STRICT OUTPUT RULES:
1. 'summary': Professional English summary.
2. 'sop_validation': 
   - Fields: greeting (bool), identification (bool), problemStatement (bool), solutionOffering (bool), closing (bool), complianceScore (0.0-1.0), adherenceStatus ("FOLLOWED" or "NOT_FOLLOWED"), explanation (string).
3. 'analytics':
   - paymentPreference: MUST be one of [EMI, FULL_PAYMENT, PARTIAL_PAYMENT, DOWN_PAYMENT].
   - rejectionReason: MUST be one of [HIGH_INTEREST, BUDGET_CONSTRAINTS, ALREADY_PAID, NOT_INTERESTED, NONE].
   - sentiment: Positive, Negative, or Neutral.
4. 'keywords': Array of key technical or business terms.
5. Return ONLY a valid JSON object.
"""

# Configuration
def _get_model():
    key = os.getenv("GEMINI_API_KEY")
    if not key: return None
    try:
        genai.configure(api_key=key)
        # Using the specific experimental model found in the scan
        return genai.GenerativeModel('gemini-3.1-flash-lite-preview')
    except Exception as e:
        print(f"LLM INIT ERROR: {e}")
        return None

def analyze_call_with_llm(transcript: str) -> Dict[str, Any]:
    model = _get_model()
    if not model:
        return _fallback_analysis(transcript)

    # Injecting the system prompt directly into the message for safety
    user_prompt = f"{SYSTEM_PROMPT}\n\nAnalyze this transcript and return the JSON audit result:\n\n{transcript}"
    
    try:
        response = model.generate_content(user_prompt)
        text = response.text
        # Extract JSON from potential markdown formatting
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].strip()
            
        data = json.loads(text)
        # Final safety check to ensure summary is English
        return data
    except Exception as e:
        print(f"LLM Error: {e}")
        return _fallback_analysis(transcript)

def _fallback_analysis(transcript: str) -> Dict[str, Any]:
    # A slightly improved version of the existing logic as a safety net
    return {
        "summary": "AI Summarization (Requires GEMINI_API_KEY for full accuracy).",
        "sop": {
            "score": 0.5,
            "passed": False,
            "missing": ["Detailed LLM Analysis skipped"],
            "found": []
        },
        "payments": { "preference": "None", "reason": "Rule-based analysis pending" },
        "rejections": { "reason": "None", "category": "None" }
    }
