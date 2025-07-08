#!/usr/bin/env python3
"""
Minimal test - just text
"""

import pytest
import sys
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.handlers.auth_handler import AuthHandler
from substack.post import Post

@pytest.mark.requires_auth
@pytest.mark.integration
async def test_minimal():
    print("🔍 Testing minimal post...")
    
    try:
        # Authenticate
        auth = AuthHandler()
        client = await auth.authenticate()
        user_id = client.get_user_id()
        
        # Create the simplest possible post
        post = Post(
            title="Minimal Test",
            subtitle="Just plain text",
            user_id=user_id
        )
        
        # Add only one paragraph
        post.paragraph("This is a single paragraph of plain text. No formatting, no special characters.")
        
        # Create and publish
        draft_data = post.get_draft()
        result = client.post_draft(draft_data)
        draft_id = result['id']
        
        print(f"✅ Draft created: {draft_id}")
        
        # Publish
        pub_result = client.publish_draft(draft_id)
        
        print(f"✅ Published: {pub_result['id']}")
        print(f"🔗 URL: https://neroaugustus.substack.com/p/{pub_result.get('slug')}")
        
        # Also try fetching a post that we know displays correctly
        print("\n📖 Fetching a known good post for comparison...")
        
        # List recent posts to find one that displays
        posts = list(client.get_posts(limit=10))
        print(f"\nRecent posts:")
        for p in posts[:5]:
            print(f"  - {p.get('title')} (ID: {p.get('id')})")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_minimal())