#!/usr/bin/env python3
"""
Debug the body field issue
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

async def debug_body_field():
    print("🔍 Debugging body field...")
    
    try:
        # Authenticate
        auth = AuthHandler()
        client = await auth.authenticate()
        user_id = client.get_user_id()
        
        # Create a post with content
        post = Post(
            title="Body Field Debug",
            subtitle="What's in the body field?",
            user_id=user_id
        )
        
        # Add content
        post.paragraph("First paragraph here.")
        post.heading("Test Heading", 2)
        post.paragraph("Second paragraph here.")
        
        # Get draft and create
        draft_data = post.get_draft()
        result = client.post_draft(draft_data)
        draft_id = result.get('id')
        print(f"✅ Draft created: {draft_id}")
        
        # Fetch it back
        fetched = client.get_draft(draft_id)
        
        # Examine the body field
        body = fetched.get('body', '')
        draft_body = fetched.get('draft_body', '')
        
        print(f"\n📄 'body' field: '{body}' (length: {len(body)})")
        print(f"📄 'draft_body' field length: {len(draft_body)}")
        
        # Parse draft_body
        if draft_body:
            try:
                parsed = json.loads(draft_body)
                print(f"\n📊 Parsed draft_body type: {parsed.get('type')}")
                print(f"📊 Content blocks: {len(parsed.get('content', []))}")
                
                # Show first block
                if parsed.get('content'):
                    first_block = parsed['content'][0]
                    print(f"\n🔍 First block:")
                    print(json.dumps(first_block, indent=2))
                    
            except json.JSONDecodeError:
                print("❌ Could not parse draft_body as JSON")
        
        # Try to publish to see what happens
        print("\n🚀 Publishing draft...")
        pub_result = client.publish_draft(draft_id)
        
        # Check published post
        print(f"\n📖 Published post ID: {pub_result.get('id')}")
        print(f"📖 Published body length: {len(str(pub_result.get('body', '')))}")
        
        # Show the actual body content
        pub_body = pub_result.get('body', '')
        print(f"\n📄 Published body content: '{pub_body}'")
        
    except Exception as e:
        print(f"❌ Debug failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_body_field())