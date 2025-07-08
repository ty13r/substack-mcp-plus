#!/usr/bin/env python3
"""
Test the fixed image upload functionality
"""

import pytest
import sys
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.handlers.auth_handler import AuthHandler
from src.handlers.image_handler import ImageHandler


@pytest.mark.requires_auth
@pytest.mark.integration
async def test_image_upload():
    # First, let's test with a simple URL
    print("Testing image upload with URL...")

    auth = AuthHandler()
    client = await auth.authenticate()

    image_handler = ImageHandler(client)

    try:
        # Test with a simple image URL
        test_url = "https://via.placeholder.com/150x150.png"

        print(f"Uploading image from URL: {test_url}")
        result = await image_handler.upload_image(test_url)

        print(f"✅ Upload successful!")
        print(f"URL: {result.get('url')}")
        print(f"Filename: {result.get('filename')}")

    except Exception as e:
        print(f"❌ Upload failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_image_upload())
