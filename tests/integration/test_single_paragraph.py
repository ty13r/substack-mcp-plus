#!/usr/bin/env python3
"""
Test creating formatted paragraphs differently
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
async def test_single_paragraph():
    print("🔍 Testing different paragraph creation approach...")

    try:
        # Authenticate
        auth = AuthHandler()
        client = await auth.authenticate()
        user_id = client.get_user_id()

        # Test using add() method with full paragraph structure
        print("\n1️⃣ Using add() method with full structure...")
        post = Post(
            title="Single Paragraph Test",
            subtitle="Testing add() method",
            user_id=user_id,
        )

        # Add a paragraph with formatting using add()
        post.add(
            {
                "type": "paragraph",
                "content": [
                    {"type": "text", "text": "This is "},
                    {"type": "text", "text": "bold", "marks": [{"type": "strong"}]},
                    {"type": "text", "text": " and "},
                    {"type": "text", "text": "italic", "marks": [{"type": "em"}]},
                    {"type": "text", "text": " text."},
                ],
            }
        )

        # Add a link
        post.add(
            {
                "type": "paragraph",
                "content": [
                    {"type": "text", "text": "Here is a "},
                    {
                        "type": "text",
                        "text": "link to Substack",
                        "marks": [
                            {"type": "link", "attrs": {"href": "https://substack.com"}}
                        ],
                    },
                    {"type": "text", "text": "."},
                ],
            }
        )

        # Add blockquote
        post.add(
            {
                "type": "blockquote",
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {"type": "text", "text": "This is a proper blockquote."}
                        ],
                    }
                ],
            }
        )

        # Create and publish
        draft_data = post.get_draft()
        result = client.post_draft(draft_data)
        pub = client.publish_draft(result["id"])

        print(f"\n✅ Published: https://neroaugustus.substack.com/p/{pub.get('slug')}")

        # Check the structure
        body = json.loads(draft_data["draft_body"])
        print(f"\n📊 Created {len(body['content'])} blocks with proper formatting")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_single_paragraph())
