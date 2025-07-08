#!/usr/bin/env python3
"""
Debug PostHandler to see what's happening
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
from substack.post import Post


async def debug_posthandler():
    print("🔍 Debugging PostHandler...")

    try:
        # Authenticate and create handler
        auth = AuthHandler()
        client = await auth.authenticate()
        post_handler = PostHandler(client)

        # Simple test content
        test_content = """# Test Post

This is a paragraph.

## Section 1

Another paragraph here."""

        # Test the conversion process
        print("\n1️⃣ Testing markdown conversion...")
        blocks = post_handler._convert_content_to_blocks(test_content, "markdown")
        print(f"Converted to {len(blocks)} blocks")

        for i, block in enumerate(blocks):
            print(f"\nBlock {i}:")
            print(f"  Type: {block.get('type')}")
            print(f"  Content: {block.get('content')}")

        # Now test creating a post manually
        print("\n2️⃣ Creating post manually...")
        user_id = client.get_user_id()
        post = Post(
            title="Manual Debug Test",
            subtitle="Testing manual creation",
            user_id=user_id,
        )

        # Add blocks manually
        print("\n3️⃣ Adding blocks to post...")
        post_handler._add_blocks_to_post(post, blocks)

        # Get draft data
        draft_data = post.get_draft()
        print(f"\n4️⃣ Draft data body length: {len(draft_data.get('draft_body', ''))}")

        # Parse and check
        body_json = json.loads(draft_data["draft_body"])
        print(f"Draft body has {len(body_json.get('content', []))} blocks")

        # Create and publish
        print("\n5️⃣ Creating draft...")
        result = client.post_draft(draft_data)
        draft_id = result.get("id")
        print(f"Draft created: {draft_id}")

        print("\n6️⃣ Publishing...")
        pub_result = client.publish_draft(draft_id)
        print(f"Published: {pub_result.get('id')}")

        # Check if body exists
        if "body" in pub_result:
            body = pub_result["body"]
            if isinstance(body, str):
                body_json = json.loads(body)
                print(
                    f"\n✅ Published with {len(body_json.get('content', []))} content blocks"
                )
            else:
                print(f"\n✅ Published with body type: {type(body)}")
        else:
            print("\n❌ No body in published result!")

    except Exception as e:
        print(f"❌ Debug failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(debug_posthandler())
