#!/usr/bin/env python3
"""
Debug Post object behavior
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
async def test_post_object():
    print("🔍 Testing Post object behavior...")

    try:
        # Authenticate
        auth = AuthHandler()
        client = await auth.authenticate()
        user_id = client.get_user_id()

        print(f"User ID: {user_id}")

        # Create Post object
        post = Post(
            title="Post Object Debug",
            subtitle="Testing Post internals",
            user_id=user_id,
        )

        # Check initial state
        print("\n📊 Initial Post state:")
        print(f"  draft_title: {post.draft_title}")
        print(f"  draft_subtitle: {post.draft_subtitle}")
        print(f"  draft_body type: {type(post.draft_body)}")

        # Add content
        print("\n📝 Adding content...")
        post.paragraph("First paragraph.")

        # Check state after adding content
        draft_before = post.get_draft()
        print(f"\n📄 After adding paragraph:")
        print(f"  draft_body in get_draft: {'draft_body' in draft_before}")

        if "draft_body" in draft_before:
            body_str = draft_before["draft_body"]
            body_data = json.loads(body_str)
            print(f"  Content blocks: {len(body_data.get('content', []))}")
            print(f"  First block: {json.dumps(body_data['content'][0], indent=2)}")

        # Now test our PostHandler to see if it's doing something different
        print("\n\n🧪 Testing PostHandler...")
        from src.handlers.post_handler import PostHandler

        post_handler = PostHandler(client)

        # Simple markdown
        markdown = "# Test\n\nThis is a paragraph."

        # Create draft using PostHandler
        result = await post_handler.create_draft(
            title="PostHandler Debug",
            content=markdown,
            subtitle="Testing handler",
            content_type="markdown",
        )

        print(f"\n✅ PostHandler created draft: {result.get('id')}")

        # Check what was created
        draft = client.get_draft(result["id"])
        if "draft_body" in draft:
            body_data = json.loads(draft["draft_body"])
            print(f"  Content blocks: {len(body_data.get('content', []))}")

            # Check the structure
            for i, block in enumerate(body_data.get("content", [])):
                print(f"\n  Block {i}:")
                print(f"    Type: {block.get('type')}")
                if block.get("type") == "paragraph" and "content" in block:
                    # This is where the issue might be
                    print(
                        f"    Content structure: {json.dumps(block['content'], indent=6)}"
                    )

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_post_object())
