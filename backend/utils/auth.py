import os
from fastapi import Header, HTTPException
from dotenv import load_dotenv

load_dotenv()

def verify_api_key(
    x_api_key: str = Header(None, alias="x-api-key"),
    authorization: str = Header(None, alias="Authorization")
):
    provided_key = x_api_key or authorization
    print("DEBUG HEADER RECEIVED:", provided_key)

    if not provided_key:
        raise HTTPException(status_code=401, detail="Missing API key")

    # Only use ENV key (secure)
    API_KEY = os.getenv("API_KEY")

    if not API_KEY:
        raise HTTPException(status_code=500, detail="Server API key not configured")

    if provided_key.strip() != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    return True