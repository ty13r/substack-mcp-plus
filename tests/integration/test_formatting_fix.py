#!/usr/bin/env python3
"""
Test how to properly handle formatting
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
async def test_formatting_fix():
    print("🔍 Testing proper formatting...")

    try:
        # Authenticate
        auth = AuthHandler()
        client = await auth.authenticate()
        user_id = client.get_user_id()

        # Create post
        post = Post(
            title="Formatting Fix Test",
            subtitle="Testing proper text formatting",
            user_id=user_id,
        )

        # Test 1: Simple paragraph with formatting using marks
        print("\n1️⃣ Testing formatted text with marks...")
        para = post.paragraph()
        para.text("This is ")
        para.text("bold text", marks=[{"type": "strong"}])
        para.text(" and this is ")
        para.text("italic text", marks=[{"type": "em"}])
        para.text(". We can also have ")
        para.text("bold and italic", marks=[{"type": "strong"}, {"type": "em"}])
        para.text(" combined.")

        # Test 2: Inline code
        para2 = post.paragraph()
        para2.text("Here's some ")
        para2.text("inline code", marks=[{"type": "code"}])
        para2.text(" mixed with regular text.")

        # Test 3: Link
        para3 = post.paragraph()
        para3.text("Here's a ")
        para3.text(
            "link to Substack", marks=[{"type": "link", "href": "https://substack.com"}]
        )
        para3.text(".")

        # Test 4: Blockquote - try using add()
        print("\n2️⃣ Testing blockquote...")
        post.add(
            {
                "type": "blockquote",
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": "This is a blockquote. It should appear indented.",
                            }
                        ],
                    }
                ],
            }
        )

        # Get draft and inspect
        draft_data = post.get_draft()
        body_json = json.loads(draft_data["draft_body"])

        print("\n📊 Generated structure:")
        print(json.dumps(body_json, indent=2))

        # Create and publish
        print("\n🚀 Creating and publishing...")
        result = client.post_draft(draft_data)
        draft_id = result.get("id")

        pub_result = client.publish_draft(draft_id)
        print(f"✅ Published: {pub_result.get('id')}")

        slug = pub_result.get("slug")
        if slug:
            print(f"🔗 URL: https://neroaugustus.substack.com/p/{slug}")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_formatting_fix())
