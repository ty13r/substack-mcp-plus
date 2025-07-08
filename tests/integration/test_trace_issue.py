#!/usr/bin/env python3
"""
Trace the exact issue
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
from src.converters.markdown_converter import MarkdownConverter
from substack.post import Post

async def trace_issue():
    print("🔍 Tracing the exact issue...")
    
    try:
        # Authenticate
        auth = AuthHandler()
        client = await auth.authenticate()
        user_id = client.get_user_id()
        
        # Test markdown conversion first
        print("\n1️⃣ Testing markdown conversion...")
        converter = MarkdownConverter()
        markdown = "This is a **bold** paragraph."
        
        blocks = converter.convert(markdown)
        print(f"Converted blocks: {json.dumps(blocks, indent=2)}")
        
        # Now test adding this to a Post
        print("\n2️⃣ Creating Post with converted content...")
        post = Post(
            title="Trace Issue Test",
            subtitle="Finding the problem",
            user_id=user_id
        )
        
        # Get the PostHandler
        post_handler = PostHandler(client)
        
        # Add blocks manually
        print("\n3️⃣ Adding blocks to post...")
        for block in blocks:
            block_type = block.get('type')
            content = block.get('content')
            
            print(f"\nProcessing block type: {block_type}")
            print(f"Content: {json.dumps(content, indent=2)}")
            
            if block_type == 'paragraph':
                para = post.paragraph()
                
                # Debug what we're passing
                print(f"Calling _add_formatted_content_to_paragraph with content type: {type(content)}")
                
                # The issue might be here
                if isinstance(content, list):
                    for item in content:
                        print(f"  Processing item: {json.dumps(item, indent=4)}")
                        if isinstance(item, dict) and item.get('type') == 'text':
                            # THIS is where we need to look for 'content' not 'text'
                            text_content = item.get('content', '')
                            marks = item.get('marks', [])
                            
                            print(f"    Text: '{text_content}'")
                            print(f"    Marks: {marks}")
                            
                            para.text(text_content)
                            if marks:
                                para.marks(marks)
        
        # Get draft and check
        draft_data = post.get_draft()
        body_str = draft_data['draft_body']
        body_json = json.loads(body_str)
        
        print(f"\n4️⃣ Final draft body:")
        print(json.dumps(body_json, indent=2))
        
        # Create and publish
        result = client.post_draft(draft_data)
        pub = client.publish_draft(result['id'])
        
        print(f"\n✅ Published: {result['id']}")
        print(f"🔗 URL: https://neroaugustus.substack.com/p/{pub.get('slug')}")
        
    except Exception as e:
        print(f"❌ Trace failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(trace_issue())