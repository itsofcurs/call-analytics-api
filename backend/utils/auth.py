import os
from fastapi import Header, HTTPException
from dotenv import load_dotenv

load_dotenv()

TRACK_3_KEY = "sk_track3_987654321"
ENV_KEY = os.getenv("API_KEY")

def verify_api_key(x_api_key: str = Header(None, alias="x-api-key")):
    print("DEBUG HEADER RECEIVED:", x_api_key)

    if not x_api_key:
        raise HTTPException(status_code=401, detail="Missing API key")

    valid_keys = [TRACK_3_KEY]
    if ENV_KEY:
        valid_keys.append(ENV_KEY)

    if x_api_key.strip() not in valid_keys:
        raise HTTPException(status_code=401, detail="Invalid API key")

    return True