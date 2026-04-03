import json
from pydantic import ValidationError
import asyncio
from unittest.mock import MagicMock
# I can just import the logic from test script.

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from routes.analyze import CallAnalysisRequest, analyze_call

async def test():
    req = CallAnalysisRequest(
        language="Hindi",
        audioFormat="mp3",
        audioBase64=""
    )
    res = await analyze_call(req, True)
    print(res)

if __name__ == "__main__":
    asyncio.run(test())
