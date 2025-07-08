#!/usr/bin/env python3
"""
Debug why posts are suddenly empty
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
from src.handlers.post_handler import PostHandler

async def debug_empty_post():
    print("🔍 Debugging empty post issue...")
    
    try:
        # Authenticate and create handlers
        auth = AuthHandler()
        client = await auth.authenticate()
        post_handler = PostHandler(client)
        
        # Very simple test
        content = """# Debug Test

This is a simple paragraph.

## Section

Another paragraph here."""

        print("\n1️⃣ Creating draft...")
        create_result = await post_handler.create_draft(
            title="Debug Empty Post",
            content=content,
            subtitle="Why is this empty?",
            content_type="markdown"
        )
        
        draft_id = create_result.get('id')
        print(f"Draft ID: {draft_id}")
        
        # Before publishing, let's check what's in the draft
        print("\n2️⃣ Checking draft content...")
        draft = client.get_draft(draft_id)
        
        # Check draft_body
        if 'draft_body' in draft:
            draft_body = draft['draft_body']
            print(f"draft_body length: {len(draft_body)}")
            
            # Parse and display
            try:
                body_json = json.loads(draft_body)
                print(f"draft_body type: {body_json.get('type')}")
                print(f"draft_body blocks: {len(body_json.get('content', []))}")
                
                # Show the actual content
                print("\n📄 Draft body content:")
                for i, block in enumerate(body_json.get('content', [])):
                    print(f"\nBlock {i}:")
                    print(f"  Type: {block.get('type')}")
                    if 'content' in block:
                        print(f"  Content: {json.dumps(block['content'], indent=4)}")
                    if 'attrs' in block:
                        print(f"  Attrs: {block['attrs']}")
                        
            except json.JSONDecodeError as e:
                print(f"Failed to parse draft_body: {e}")
        
        # Check what create_result returned
        print(f"\n3️⃣ Create result keys: {list(create_result.keys())}")
        
        # Publish
        print("\n4️⃣ Publishing...")
        publish_result = await post_handler.publish_draft(draft_id)
        
        print(f"\n5️⃣ Publish result:")
        print(f"  ID: {publish_result.get('id')}")
        print(f"  Type: {publish_result.get('type')}")
        print(f"  Is published: {publish_result.get('is_published')}")
        
        # Check body after publish
        if 'body' in publish_result:
            body = publish_result['body']
            print(f"\n  body field exists: {body is not None}")
            print(f"  body type: {type(body)}")
            print(f"  body value: {body}")
            
            if isinstance(body, str) and body:
                try:
                    parsed_body = json.loads(body)
                    print(f"  Parsed body blocks: {len(parsed_body.get('content', []))}")
                except:
                    print("  Could not parse body as JSON")
        
        # Final URL
        slug = publish_result.get('slug')
        if slug:
            print(f"\n🔗 Post URL: https://neroaugustus.substack.com/p/{slug}")
        
    except Exception as e:
        print(f"❌ Debug failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_empty_post())