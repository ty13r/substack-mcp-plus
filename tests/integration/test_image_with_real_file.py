#!/usr/bin/env python3
"""
Test image upload with a real image file
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
async def test_real_image_upload():
    print("Testing image upload with a real image file...")
    
    auth = AuthHandler()
    client = await auth.authenticate()
    
    image_handler = ImageHandler(client)
    
    # Create a minimal PNG file (1x1 pixel transparent PNG)
    png_data = bytes.fromhex('89504e470d0a1a0a0000000d494844520000000100000001080600000037f7c24e000000124944415478da626000024000004c0001000000000000')
    
    test_file = "/tmp/test_image.png"
    with open(test_file, 'wb') as f:
        f.write(png_data)
    
    try:
        print(f"Uploading real PNG file: {test_file}")
        
        result = await image_handler.upload_image(test_file)
        
        print(f"✅ Real image upload successful!")
        print(f"   Substack URL: {result.get('url')}")
        print(f"   Image ID: {result.get('id')}")
        print(f"   Size: {result.get('width')}x{result.get('height')}")
        print(f"   Content type: {result.get('content_type')}")
        
        # Clean up
        os.unlink(test_file)
        
        return result.get('url')  # Return URL for use in a post
        
    except Exception as e:
        print(f"❌ Real image upload failed: {e}")
        return None

if __name__ == "__main__":
    asyncio.run(test_real_image_upload())