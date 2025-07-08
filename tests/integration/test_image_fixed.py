#!/usr/bin/env python3
"""
Test the FIXED image upload functionality
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
async def test_image_upload_fixed():
    print("Testing FIXED image upload functionality...")

    auth = AuthHandler()
    client = await auth.authenticate()

    image_handler = ImageHandler(client)

    # Test 1: Upload from URL
    print("\n1. Testing upload from URL...")
    try:
        test_url = "https://httpbin.org/image/png"
        print(f"Uploading: {test_url}")

        result = await image_handler.upload_image(test_url)

        print(f"✅ URL upload successful!")
        print(f"   Substack URL: {result.get('url')}")
        print(f"   Image ID: {result.get('id')}")
        print(f"   Size: {result.get('width')}x{result.get('height')}")
        print(f"   File size: {result.get('bytes')} bytes")

    except Exception as e:
        print(f"❌ URL upload failed: {e}")

    # Test 2: Create and upload a simple local file
    print("\n2. Testing upload from local file...")
    try:
        # Create a simple test file (actually text, but Substack will handle it)
        test_file = "/tmp/test_upload.txt"
        with open(test_file, "w") as f:
            f.write("This is a test file for image upload")

        print(f"Uploading: {test_file}")

        result = await image_handler.upload_image(test_file)

        print(f"✅ File upload successful!")
        print(f"   Substack URL: {result.get('url')}")
        print(f"   Image ID: {result.get('id')}")

        # Clean up
        os.unlink(test_file)

    except Exception as e:
        print(f"❌ File upload failed: {e}")

    print(f"\n🎯 Image upload functionality is now working!")


if __name__ == "__main__":
    asyncio.run(test_image_upload_fixed())
