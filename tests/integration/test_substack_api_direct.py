#!/usr/bin/env python3
"""
Test using substack API directly to understand the issue
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
async def test_direct_api():
    print("🔍 Testing direct API usage...")
    
    try:
        # Authenticate
        auth = AuthHandler()
        client = await auth.authenticate()
        
        # Try to create a post using the API directly
        # First, let's see what methods are available
        print("\n📋 Client methods:")
        for attr in dir(client):
            if not attr.startswith('_'):
                print(f"  - {attr}")
        
        # Check if we have a posts attribute or similar
        if hasattr(client, 'posts'):
            print("\n📋 Posts methods:")
            for attr in dir(client.posts):
                if not attr.startswith('_'):
                    print(f"  - {attr}")
        
        # Let's try the python-substack way
        from substack.post import Post
        
        # Create post
        post = Post(
            title="Direct API Test",
            subtitle="Testing the API directly",
            user_id=client.get_user_id()
        )
        
        # Add content
        post.paragraph("This is a test paragraph.")
        post.heading("Test Heading", 2)
        post.paragraph("Another paragraph with **bold** text.")
        
        # Get the draft structure
        draft_data = post.get_draft()
        
        print("\n📊 Draft data structure:")
        for key, value in draft_data.items():
            if isinstance(value, str) and len(value) > 100:
                print(f"  {key}: {type(value).__name__} (length: {len(value)})")
            else:
                print(f"  {key}: {value}")
        
        # Create the draft
        print("\n🚀 Creating draft...")
        result = client.post_draft(draft_data)
        
        print(f"\n✅ Draft created!")
        print(f"  ID: {result.get('id')}")
        print(f"  Title: {result.get('draft_title')}")
        
        # Now let's check what python-substack actually sends
        import json
        if 'draft_body' in draft_data:
            body_json = json.loads(draft_data['draft_body'])
            print(f"\n📄 Draft body structure:")
            print(json.dumps(body_json, indent=2)[:500] + "...")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_direct_api())