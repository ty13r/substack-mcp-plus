#!/usr/bin/env python3
"""
Test proper formatting with marks
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
async def test_formatting_fix2():
    print("🔍 Testing proper formatting with marks...")

    try:
        # Authenticate
        auth = AuthHandler()
        client = await auth.authenticate()
        user_id = client.get_user_id()

        # Create post
        post = Post(
            title="Formatting Fix Test 2",
            subtitle="Testing text formatting with marks",
            user_id=user_id,
        )

        # Test chained method calls
        print("\n1️⃣ Testing chained formatting...")
        post.paragraph().text("This is ").text("bold text").marks(
            [{"type": "strong"}]
        ).text(" and this is ").text("italic text").marks([{"type": "em"}]).text(".")

        # Test inline code
        post.paragraph().text("Here's some ").text("inline code").marks(
            [{"type": "code"}]
        ).text(" mixed with regular text.")

        # Test link
        post.paragraph().text("Here's a ").text("link to Substack").marks(
            [{"type": "link", "href": "https://substack.com"}]
        ).text(".")

        # Test blockquote with proper structure
        print("\n2️⃣ Testing blockquote...")
        post.add(
            {
                "type": "blockquote",
                "content": [
                    {
                        "type": "paragraph",
                        "content": [{"type": "text", "text": "This is a blockquote."}],
                    }
                ],
            }
        )

        # Test multiple formats in one text
        post.paragraph().text("Combined: ").text("bold and italic").marks(
            [{"type": "strong"}, {"type": "em"}]
        ).text(" text.")

        # Get draft and check structure
        draft_data = post.get_draft()
        body_json = json.loads(draft_data["draft_body"])

        print("\n📊 First content block:")
        print(json.dumps(body_json["content"][0], indent=2))

        # Create and publish
        print("\n🚀 Publishing...")
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
    asyncio.run(test_formatting_fix2())
