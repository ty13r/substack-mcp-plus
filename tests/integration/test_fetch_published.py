#!/usr/bin/env python3
"""
Fetch a published post to see what's actually stored
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

async def fetch_published_post():
    print("🔍 Fetching published post...")
    
    try:
        # Authenticate
        auth = AuthHandler()
        client = await auth.authenticate()
        
        # Fetch the most recent post
        post_id = "167624887"  # The test post we just published
        
        print(f"\n📖 Fetching post {post_id}...")
        post = client.get_draft(post_id)
        
        # Check all fields
        print(f"\n📋 Post fields:")
        print(f"  is_published: {post.get('is_published')}")
        print(f"  type: {post.get('type')}")
        print(f"  title: {post.get('title')}")
        print(f"  subtitle: {post.get('subtitle')}")
        
        # Check body field
        body = post.get('body')
        draft_body = post.get('draft_body')
        
        print(f"\n📄 Content fields:")
        print(f"  body type: {type(body)}")
        print(f"  body: {body}")
        
        if draft_body:
            print(f"  draft_body length: {len(draft_body)}")
            # Parse draft_body
            try:
                parsed = json.loads(draft_body)
                print(f"  draft_body blocks: {len(parsed.get('content', []))}")
            except:
                print("  Could not parse draft_body")
        
        # Check if there's a different field for published content
        for key in post.keys():
            if 'body' in key.lower() or 'content' in key.lower():
                value = post[key]
                if value and isinstance(value, str) and len(value) > 10:
                    print(f"\n  {key}: {type(value).__name__} (length: {len(value)})")
                    if key not in ['body', 'draft_body']:
                        print(f"    Preview: {value[:100]}...")
        
    except Exception as e:
        print(f"❌ Fetch failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(fetch_published_post())