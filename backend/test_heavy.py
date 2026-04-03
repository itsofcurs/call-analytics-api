import asyncio
import base64
import time
import os
import sys

# Ensure backend folder is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from routes.analyze import analyze_call, CallAnalysisRequest

async def run_heavy_test():
    print("==================================================")
    print("HEAVY SCRIPT EXECUTION: Testing Call Analytics API")
    print("==================================================")
    
    # 1. Create a minimal dummy base64 to simulate audio payload
    # Since Whisper ignores junk content for transcript or fails, this will be excellent for testing fallback paths.
    dummy_audio = b"\x00\x01\x02\x03" * 1024  # 4KB dummy
    b64_audio = base64.b64encode(dummy_audio).decode('utf-8')
    
    print("\n[✓] Generated Payload")
    print(f"Payload Size: {len(b64_audio)} Base64 Chars")
    
    request = CallAnalysisRequest(
        language="Hindi",
        audioFormat="mp3",
        audioBase64=b64_audio
    )
    
    print("\n[>] Calling analyze_call()...")
    start_time = time.time()
    
    # Note: verify_api_key injects True normally if valid, we just pass True here
    try:
        response = await analyze_call(request, True)
    except Exception as e:
        response = {"status": "error", "message": f"Crash: {str(e)}"}
        
    duration = time.time() - start_time
    
    print(f"\n[✓] Call Complete in {duration:.2f} seconds")
    
    print("\n================  RESPONSE  ==================")
    if isinstance(response, dict):
        print("Status:", response.get("status"))
        print("Message:", response.get("message"))
    else:
        # Pydantic response
        resp_dict = response.model_dump() if hasattr(response, "model_dump") else response.dict()
        print(f"Status: {resp_dict['status']}")
        print(f"Transcript: {resp_dict['transcript'][:100]}...")
        print(f"Summary: {resp_dict['summary']}")
        print(f"Sentiment: {resp_dict['analytics']['sentiment']}")
        print(f"SOP ADHERENCE: {resp_dict['sop_validation']['adherenceStatus']} (Score: {resp_dict['sop_validation']['complianceScore']})")
        print(f"PAYMENT DETECTED: {resp_dict['analytics']['paymentPreference']}")
        print(f"REJECTION DETECTED: {resp_dict['analytics']['rejectionReason']}")
        print(f"KEYWORDS: {resp_dict['keywords']}")

if __name__ == "__main__":
    asyncio.run(run_heavy_test())
