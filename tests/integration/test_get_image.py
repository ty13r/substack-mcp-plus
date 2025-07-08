#!/usr/bin/env python3
"""
Test the get_image method to understand image handling
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
async def test_get_image():
    auth = AuthHandler()
    client = await auth.authenticate()
    
    # Check what get_image does
    try:
        help(client.get_image)
    except:
        print("No help available for get_image")
    
    # Try to call it to see what it expects
    try:
        result = client.get_image("test")
        print(f"get_image result: {result}")
    except Exception as e:
        print(f"get_image error: {e}")
        
    # Check if there are any methods in the client's class
    print(f"\nClient type: {type(client)}")

if __name__ == "__main__":
    asyncio.run(test_get_image())