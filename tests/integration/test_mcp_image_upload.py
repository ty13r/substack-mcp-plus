#!/usr/bin/env python3
"""
Test image upload through the MCP server
"""

import pytest
import sys
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.server import SubstackMCPServer

@pytest.mark.requires_auth
@pytest.mark.integration
async def test_mcp_image_upload():
    print("Testing image upload through MCP server...")
    
    # Create a test PNG file
    png_data = bytes.fromhex('89504e470d0a1a0a0000000d494844520000000100000001080600000037f7c24e000000124944415478da626000024000004c0001000000000000')
    test_file = "/tmp/test_mcp_image.png"
    with open(test_file, 'wb') as f:
        f.write(png_data)
    
    try:
        # Create MCP server instance  
        server_instance = SubstackMCPServer()
        
        # Test the upload_image tool
        arguments = {"image_path": test_file}
        
        # Access the handlers through the server
        auth_handler = server_instance.auth_handler
        client = await auth_handler.authenticate()
        
        # Import and use ImageHandler directly to test
        from src.handlers.image_handler import ImageHandler
        image_handler = ImageHandler(client)
        
        result = await image_handler.upload_image(test_file)
        
        print(f"✅ MCP image upload successful!")
        print(f"   URL: {result.get('url')}")
        print(f"   ID: {result.get('id')}")
        
        # Now test creating a post with the uploaded image
        from src.handlers.post_handler import PostHandler
        post_handler = PostHandler(client)
        
        image_url = result.get('url')
        content = f"""# Image Upload Test

This post contains an uploaded image:

![Test Image]({image_url})

The image was uploaded using our MCP server's upload_image tool!"""

        post_result = await post_handler.create_draft(
            title="🖼️ MCP Image Upload Test",
            content=content,
            subtitle="Testing image upload integration",
            content_type="markdown"
        )
        
        draft_id = post_result.get('id')
        print(f"\n✅ Post with image created!")
        print(f"   Draft ID: {draft_id}")
        
        # Publish the post
        publish_result = await post_handler.publish_draft(draft_id)
        
        slug = publish_result.get('slug')
        if slug:
            print(f"🔗 Post URL: https://neroaugustus.substack.com/p/{slug}")
        
        # Clean up
        os.unlink(test_file)
        
    except Exception as e:
        print(f"❌ MCP image upload failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_mcp_image_upload())