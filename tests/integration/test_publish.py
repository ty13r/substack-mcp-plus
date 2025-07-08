#!/usr/bin/env python3
"""
Test publishing the debug draft to see if content appears
"""

import pytest
import sys
import os
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.handlers.auth_handler import AuthHandler

@pytest.mark.requires_auth
@pytest.mark.integration
async def test_publish():
    """Test publishing the debug draft"""
    # Authenticate
    auth_handler = AuthHandler()
    client = await auth_handler.authenticate()
    
    # Publish the test draft
    draft_id = "167621241"
    
    try:
        result = client.publish_draft(draft_id)
        print(f"Published draft {draft_id}")
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error publishing: {e}")

if __name__ == "__main__":
    asyncio.run(test_publish())