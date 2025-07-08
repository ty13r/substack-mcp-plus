#!/usr/bin/env python3
"""
Test fetching individual posts
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

@pytest.mark.requires_auth
@pytest.mark.integration
async def test_individual_fetch():
    print("🔍 Testing individual post fetching...")
    
    try:
        # Authenticate
        auth = AuthHandler()
        client = await auth.authenticate()
        
        # Known post IDs
        test_posts = [
            ("167625322", "Fixed Formatting Test"),
            ("167618884", "Early working test"),
            ("167606195", "83 Attempts post")
        ]
        
        for post_id, description in test_posts:
            print(f"\n📄 Fetching {description} (ID: {post_id})...")
            
            try:
                post = client.get_draft(post_id)
                
                print(f"  Type: {post.get('type')}")
                print(f"  Is published: {post.get('is_published')}")
                print(f"  Editor v2: {post.get('editor_v2')}")
                
                # Check body
                body = post.get('body')
                draft_body = post.get('draft_body')
                
                if body:
                    print(f"  Body: {type(body).__name__}")
                    if isinstance(body, str):
                        try:
                            parsed = json.loads(body)
                            content_blocks = parsed.get('content', [])
                            print(f"  Content blocks: {len(content_blocks)}")
                            
                            # Check if content is actually empty
                            total_text = 0
                            for block in content_blocks:
                                if 'content' in block:
                                    total_text += len(str(block['content']))
                            print(f"  Total content length: {total_text}")
                            
                        except:
                            print(f"  Body is string but not JSON: {body[:100]}...")
                else:
                    print(f"  Body: None or empty")
                    
                if draft_body:
                    print(f"  Draft body: exists (length: {len(draft_body)})")
                else:
                    print(f"  Draft body: None or empty")
                    
            except Exception as e:
                print(f"  Error fetching: {e}")
        
        # Now let's check if there's a publication setting issue
        print("\n\n🔍 Checking publication settings...")
        user_id = client.get_user_id()
        print(f"User ID: {user_id}")
        
        # Try to get publication info
        try:
            # Get user profile
            profile = client.get_user_profile()
            print(f"Profile type: {type(profile)}")
            
        except Exception as e:
            print(f"Could not get profile: {e}")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_individual_fetch())