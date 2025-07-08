#!/usr/bin/env python3
"""
Test simple code block to debug the issue
"""

import pytest
import sys
import os
import asyncio
import json
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.handlers.auth_handler import AuthHandler
from substack.post import Post

@pytest.mark.requires_auth
@pytest.mark.integration
async def test_simple_code_block():
    print("🧪 Testing simple code block...")
    
    # Authenticate
    auth = AuthHandler()
    client = await auth.authenticate()
    user_id = client.get_user_id()
    
    # Create a very simple post with just code
    post = Post(
        title="Simple Code Block Test",
        subtitle="Testing minimal code block",
        user_id=user_id
    )
    
    # Method 1: Direct add with code_block
    print("\n📝 Method 1: Direct code_block add...")
    post.add({
        'type': 'code_block',
        'content': 'def hello():\n    print("Hello World")\n    return True',
        'attrs': {'language': 'python'}
    })
    
    # Add a paragraph
    post.paragraph("Between code blocks")
    
    # Method 2: Alternative structure
    print("📝 Method 2: Alternative structure...")
    post.add({
        'type': 'code_block',
        'content': [
            {
                'type': 'text',
                'text': 'function test() {\n    console.log("Test");\n}'
            }
        ]
    })
    
    # Get draft and examine structure
    draft_data = post.get_draft()
    body_json = json.loads(draft_data.get('draft_body', '{}'))
    
    print("\n📄 Generated structure:")
    print(json.dumps(body_json, indent=2))
    
    # Create the actual draft
    print("\n🚀 Creating draft...")
    result = client.post_draft(draft_data)
    draft_id = result.get('id')
    print(f"✅ Draft created: {draft_id}")
    
    # Publish it
    print("🚀 Publishing...")
    publish_result = client.publish_draft(draft_id)
    
    slug = publish_result.get('slug')
    if slug:
        print(f"✅ Published: https://neroaugustus.substack.com/p/{slug}")
    
    print("\n🎯 Check if code blocks appear correctly!")

if __name__ == "__main__":
    asyncio.run(test_simple_code_block())