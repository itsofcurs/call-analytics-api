# Main Feature Testing Guide (Postman)

This guide tests every required feature one by one:
- Voice-to-Text (Hinglish/Tanglish)
- Text Summarization
- SOP Validation
- Payment Categorization
- Rejection Analysis

## 1) Prerequisites

Run all required services before opening Postman.

### Backend API
From `backend/`:

```powershell
$env:API_KEY="hackathon123"
$env:CELERY_BROKER_URL="redis://localhost:6379/0"
$env:CELERY_RESULT_BACKEND="redis://localhost:6379/0"
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Celery Worker
Open a second terminal in `backend/`:

```powershell
$env:API_KEY="hackathon123"
$env:CELERY_BROKER_URL="redis://localhost:6379/0"
$env:CELERY_RESULT_BACKEND="redis://localhost:6379/0"
celery -A tasks.celery_app worker --loglevel=info
```

### Redis
Make sure Redis is running locally on `localhost:6379`.

## 2) Import into Postman

Import both files:
- `postman/CallCenter-Feature-Tests.postman_collection.json`
- `postman/CallCenter-Feature-Tests.postman_environment.json`

Select environment: `CallCenter Local`

## 3) Request Order (Run One by One)

1. `00 - Health`
2. `01 - Analyze Audio (Hinglish/Tanglish) - Queue`
3. `02 - Poll Job Status` (repeat until `status=success`)
4. `03 - Analyze Document (Summary + Sentiment + Entities)`
5. Negative tests: `04`, `05`, `06`

## 4) Requirement-wise Validation

## A) Voice-to-Text (Hinglish/Tanglish)
Request: `01` then `02`

Pass criteria:
- `02` returns `status=success`
- `result.transcript` is non-empty
- Transcript should preserve mixed-language context from your source audio

Manual checks:
- Hinglish sample should include Roman Hindi words/phrases from the call
- Tanglish sample should include Roman Tamil words/phrases from the call

## B) Text Summarization
Request: `02` (audio path) and `03` (document path)

Pass criteria:
- `result.summary` (audio) is non-empty
- `summary` (document) is non-empty
- Summary captures core intent: customer need + agent action + outcome

## C) SOP Validation
Request: `02`

Pass criteria:
- `result.sop` object exists
- `result.sop.score` present
- `result.sop.passed` boolean present
- `result.sop.missing` array present

Current configured SOP phrases (default):
- greeting
- verify customer details
- explain product
- mention payment options
- offer emi
- confirm next steps

Expected logic:
- score is based on phrase coverage and ordering
- pass threshold: `min_score = 0.7`

## D) Payment Categorization
Request: `02`

Pass criteria:
- `result.payments.counts` has keys: `emi`, `full`, `partial`, `down`
- `result.payments.mentions` contains matched phrases

Matching patterns currently implemented:
- `emi`: "emi", "installment", "monthly payment"
- `full`: "full payment", "paid in full", "one time"
- `partial`: "partial payment", "part payment", "advance"
- `down`: "down payment", "token amount", "booking amount"

## E) Rejection Analysis
Request: `02`

Pass criteria:
- `result.rejections.reasons` exists
- `result.rejections.categories` includes `price`, `timing`, `trust`, `need`

Matching patterns currently implemented:
- `price`: "too expensive", "cost too high", "price issue"
- `timing`: "call later", "busy", "not now"
- `trust`: "dont trust", "scam", "fraud"
- `need`: "dont need", "not interested", "no need"

## 5) Negative/Guard Tests

- `04 - Negative: Missing API Key` -> should return `401`
- `05 - Negative: Unsupported Audio Type` -> should return `400`
- `06 - Negative: Unsupported Document Type` -> should return `400`

These confirm auth and file-type validation requirements.

## 6) Suggested Test Data

Prepare at least these audio files:
- `hinglish_call_1.wav` (contains payment + one rejection phrase)
- `tanglish_call_1.wav` (contains SOP phrases + payment mentions)

For stronger validation, include scripted phrases that map to each category above.

## 7) Result Recording Template

Use this simple matrix during testing:

| Requirement | Request(s) | Status | Evidence |
|---|---|---|---|
| Voice-to-Text (Hinglish) | 01 + 02 | Pass/Fail | transcript snippet |
| Voice-to-Text (Tanglish) | 01 + 02 | Pass/Fail | transcript snippet |
| Summarization | 02/03 | Pass/Fail | summary snippet |
| SOP Validation | 02 | Pass/Fail | sop.score + sop.missing |
| Payment Categorization | 02 | Pass/Fail | payments.counts |
| Rejection Analysis | 02 | Pass/Fail | rejections.categories |

## 8) Common Failure Causes

- `jobs` always `pending` -> Celery worker or Redis not running
- `401` on all requests -> API key mismatch between Postman and backend env
- `500` on audio -> Whisper model load/runtime issue
- weak transcript quality -> noisy/low-volume source audio, language mix complexity

