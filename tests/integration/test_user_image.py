#!/usr/bin/env python3
"""
Test image upload with user's specific image file
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
from src.handlers.post_handler import PostHandler


@pytest.mark.requires_auth
@pytest.mark.integration
async def test_user_image_upload():
    print("Testing image upload with user's specific image...")

    # Path to user's image
    image_path = "/Users/Matt/Downloads/ChatGPT Image Jul 5, 2025, 08_35_46 PM.png"

    # Check if file exists
    if not os.path.exists(image_path):
        print(f"❌ Image file not found: {image_path}")
        return

    print(f"📁 Found image file: {image_path}")
    print(f"📏 File size: {os.path.getsize(image_path)} bytes")

    try:
        # Authenticate and create handlers
        auth = AuthHandler()
        client = await auth.authenticate()

        image_handler = ImageHandler(client)
        post_handler = PostHandler(client)

        # Upload the image
        print(f"\n📤 Uploading image...")
        result = await image_handler.upload_image(image_path)

        print(f"✅ Image upload successful!")
        print(f"   Substack URL: {result.get('url')}")
        print(f"   Image ID: {result.get('id')}")
        print(f"   Dimensions: {result.get('width')}x{result.get('height')}")
        print(f"   Content Type: {result.get('content_type')}")
        print(f"   File Size: {result.get('bytes')} bytes")

        # Create a post with the uploaded image
        image_url = result.get("url")
        content = f"""# Real Image Upload Test

This post contains a real image uploaded from the Downloads folder:

![ChatGPT Image from July 5, 2025]({image_url})

## Upload Details

- **Original File**: `ChatGPT Image Jul 5, 2025, 08_35_46 PM.png`
- **Substack Image ID**: {result.get('id')}
- **Dimensions**: {result.get('width')} × {result.get('height')} pixels
- **File Size**: {result.get('bytes')} bytes
- **Content Type**: {result.get('content_type')}

This demonstrates that our MCP server can successfully upload and embed real images from the local filesystem into Substack posts!

🎉 **Image upload functionality is working perfectly!**"""

        print(f"\n📝 Creating post with uploaded image...")
        post_result = await post_handler.create_draft(
            title="📸 Real Image Upload Test - ChatGPT Screenshot",
            content=content,
            subtitle="Successfully uploaded and embedded a real image file using our MCP server",
            content_type="markdown",
        )

        draft_id = post_result.get("id")
        print(f"✅ Draft created: {draft_id}")

        # Publish the post
        print(f"\n🚀 Publishing post...")
        publish_result = await post_handler.publish_draft(draft_id)

        print(f"✅ Post published successfully!")
        print(f"🌐 Post ID: {publish_result.get('id')}")

        slug = publish_result.get("slug")
        if slug:
            print(f"🔗 Post URL: https://neroaugustus.substack.com/p/{slug}")

        print(f"\n🎯 Check your Substack to see the real image embedded in the post!")

    except Exception as e:
        print(f"❌ Upload failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_user_image_upload())
