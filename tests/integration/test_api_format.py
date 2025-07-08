#!/usr/bin/env python3
"""
Test what format Substack actually expects
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
async def test_api_format():
    print("🔍 Testing Substack API format...")

    try:
        # Authenticate
        auth = AuthHandler()
        client = await auth.authenticate()
        user_id = client.get_user_id()

        # Method 1: Using Post object with simple content
        print("\n1️⃣ Method 1: Post object with simple methods...")
        post1 = Post(
            title="API Format Test 1",
            subtitle="Using Post object methods",
            user_id=user_id,
        )

        post1.paragraph("Simple paragraph.")
        post1.heading("Test Heading", 2)
        post1.paragraph("Another paragraph.")

        draft_data1 = post1.get_draft()
        result1 = client.post_draft(draft_data1)
        draft_id1 = result1.get("id")

        # Publish and check
        pub1 = client.publish_draft(draft_id1)
        print(f"✅ Method 1 published: {draft_id1}")

        # Method 2: Direct API call with manual structure
        print("\n2️⃣ Method 2: Direct API with manual structure...")

        manual_body = {
            "type": "doc",
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {"type": "text", "text": "This is "},
                        {"type": "text", "text": "bold", "marks": [{"type": "strong"}]},
                        {"type": "text", "text": " text."},
                    ],
                },
                {
                    "type": "heading",
                    "attrs": {"level": 2},
                    "content": [{"type": "text", "text": "Manual Heading"}],
                },
                {
                    "type": "blockquote",
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {"type": "text", "text": "This is a blockquote."}
                            ],
                        }
                    ],
                },
            ],
        }

        manual_draft = {
            "draft_title": "API Format Test 2",
            "draft_subtitle": "Manual structure test",
            "draft_body": json.dumps(manual_body),
            "draft_bylines": [{"id": user_id, "is_guest": False}],
            "audience": "everyone",
            "draft_section_id": None,
            "section_chosen": True,
            "write_comment_permissions": "everyone",
        }

        result2 = client.post_draft(manual_draft)
        draft_id2 = result2.get("id")

        # Publish
        pub2 = client.publish_draft(draft_id2)
        print(f"✅ Method 2 published: {draft_id2}")

        # Compare the results
        print("\n📊 Comparing published posts...")

        # Fetch both back
        post1_data = client.get_draft(draft_id1)
        post2_data = client.get_draft(draft_id2)

        print(f"\nPost 1 body type: {type(post1_data.get('body'))}")
        print(f"Post 2 body type: {type(post2_data.get('body'))}")

        if post1_data.get("body"):
            body1 = (
                json.loads(post1_data["body"])
                if isinstance(post1_data["body"], str)
                else post1_data["body"]
            )
            print(f"Post 1 content blocks: {len(body1.get('content', []))}")

        if post2_data.get("body"):
            body2 = (
                json.loads(post2_data["body"])
                if isinstance(post2_data["body"], str)
                else post2_data["body"]
            )
            print(f"Post 2 content blocks: {len(body2.get('content', []))}")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_api_format())
