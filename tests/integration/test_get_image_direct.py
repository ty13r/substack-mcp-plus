#!/usr/bin/env python3
"""
Test get_image method directly to understand how it works
"""

import pytest
import sys
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.handlers.auth_handler import AuthHandler

@pytest.mark.requires_auth
@pytest.mark.integration
async def test_get_image_direct():
    auth = AuthHandler()
    client = await auth.authenticate()
    
    # Test with a well-known URL
    print("Testing client.get_image with a working URL...")
    
    try:
        # Use a simple, working image URL
        test_url = "https://httpbin.org/image/png"
        
        print(f"Testing with URL: {test_url}")
        result = client.get_image(test_url)
        
        print(f"✅ get_image result: {result}")
        print(f"Type: {type(result)}")
        
    except Exception as e:
        print(f"❌ get_image failed: {e}")
        import traceback
        traceback.print_exc()
        
    # Also test with a local file if we have one
    print("\nTesting with a simple local file...")
    
    try:
        # Create a simple test file
        test_file = "/tmp/test_image.txt"
        with open(test_file, 'w') as f:
            f.write("test image content")
        
        result = client.get_image(test_file)
        print(f"✅ get_image with file result: {result}")
        
        # Clean up
        os.unlink(test_file)
        
    except Exception as e:
        print(f"❌ get_image with file failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_get_image_direct())