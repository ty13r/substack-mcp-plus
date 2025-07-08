#!/usr/bin/env python3
"""
Investigate what changed
"""

import pytest
import sys
import os
import asyncio
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.handlers.auth_handler import AuthHandler

async def investigate_issue():
    print("🔍 Investigating the issue...")
    
    try:
        # Authenticate
        auth = AuthHandler()
        client = await auth.authenticate()
        
        # Get publication info
        print("\n📊 Publication info:")
        pub_url = client.get_publication_url()
        print(f"Publication URL: {pub_url}")
        
        # Check recent posts
        print("\n📋 Checking recent posts...")
        posts = list(client.get_posts())[:5]  # Get last 5
        
        for post in posts:
            post_id = post.get('id')
            title = post.get('title', 'Untitled')
            is_published = post.get('is_published', False)
            post_date = post.get('post_date', '')
            
            print(f"\n📄 Post: {title}")
            print(f"   ID: {post_id}")
            print(f"   Published: {is_published}")
            print(f"   Date: {post_date}")
            
            # Check if it has body content
            if 'body' in post:
                body = post['body']
                if body:
                    try:
                        if isinstance(body, str):
                            body_data = json.loads(body)
                            content_count = len(body_data.get('content', []))
                            print(f"   Content blocks: {content_count}")
                        else:
                            print(f"   Body type: {type(body)}")
                    except:
                        print(f"   Body exists but couldn't parse")
                else:
                    print(f"   Body is empty/null")
            else:
                print(f"   No body field")
        
        # Create a test post and monitor the response
        print("\n\n🧪 Creating test post and monitoring...")
        from substack.post import Post
        
        post = Post(
            title=f"Debug Test {datetime.now().strftime('%H:%M:%S')}",
            subtitle="Monitoring the creation process",
            user_id=client.get_user_id()
        )
        
        post.paragraph("Test paragraph one.")
        post.paragraph("Test paragraph two.")
        
        # Get draft data
        draft_data = post.get_draft()
        
        # Create draft
        print("\n📝 Creating draft...")
        create_response = client.post_draft(draft_data)
        
        print(f"Create response type: {type(create_response)}")
        print(f"Has body in response: {'body' in create_response}")
        
        # Publish
        draft_id = create_response['id']
        print(f"\n🚀 Publishing draft {draft_id}...")
        
        publish_response = client.publish_draft(draft_id)
        
        print(f"Publish response type: {type(publish_response)}")
        print(f"Published ID: {publish_response.get('id')}")
        print(f"Has body: {'body' in publish_response}")
        
        if 'body' in publish_response and publish_response['body']:
            print("✅ Body content exists in response")
        else:
            print("❌ No body content in response")
            
    except Exception as e:
        print(f"❌ Investigation failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(investigate_issue())