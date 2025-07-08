#!/usr/bin/env python3
"""
Test with absolute minimal content
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
async def test_absolute_minimal():
    print("🔍 Testing absolute minimal post...")

    try:
        # Authenticate
        auth = AuthHandler()
        client = await auth.authenticate()
        user_id = client.get_user_id()

        # Create the simplest possible post using direct API
        print("\n1️⃣ Creating minimal post with direct API...")

        # Manually create the exact structure
        body = {
            "type": "doc",
            "content": [
                {
                    "type": "paragraph",
                    "content": [{"type": "text", "text": "This is a test."}],
                }
            ],
        }

        draft_data = {
            "draft_title": "Minimal API Test",
            "draft_subtitle": "Testing with minimal content",
            "draft_body": json.dumps(body),
            "draft_bylines": [{"id": user_id, "is_guest": False}],
            "audience": "everyone",
            "draft_section_id": None,
            "section_chosen": True,
            "write_comment_permissions": "everyone",
        }

        # Create draft
        result = client.post_draft(draft_data)
        draft_id = result["id"]
        print(f"✅ Draft created: {draft_id}")

        # Publish
        pub_result = client.publish_draft(draft_id)
        print(f"✅ Published: {pub_result['id']}")
        print(f"🔗 URL: https://neroaugustus.substack.com/p/{pub_result.get('slug')}")

        # Verify what was stored
        fetched = client.get_draft(draft_id)
        if fetched.get("body"):
            stored_body = json.loads(fetched["body"])
            print(f"\n📄 Stored body has {len(stored_body.get('content', []))} blocks")

        # Now try with Post object
        print("\n\n2️⃣ Creating with Post object...")

        post = Post(
            title="Post Object Minimal Test",
            subtitle="Using Post object",
            user_id=user_id,
        )

        # Just one paragraph
        post.paragraph("This is a test using Post object.")

        draft_data2 = post.get_draft()
        result2 = client.post_draft(draft_data2)
        draft_id2 = result2["id"]

        pub_result2 = client.publish_draft(draft_id2)
        print(f"✅ Published: {pub_result2['id']}")
        print(f"🔗 URL: https://neroaugustus.substack.com/p/{pub_result2.get('slug')}")

        # Compare the two
        print("\n\n📊 Comparing both posts...")
        post1 = client.get_draft(draft_id)
        post2 = client.get_draft(draft_id2)

        body1 = post1.get("body", "")
        body2 = post2.get("body", "")

        print(f"Post 1 body length: {len(body1)}")
        print(f"Post 2 body length: {len(body2)}")

        if body1 == body2:
            print("✅ Bodies are identical")
        else:
            print("❌ Bodies are different")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_absolute_minimal())
