#!/usr/bin/env python3
"""
Test reverting to simpler approach
"""

import pytest
import sys
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.handlers.auth_handler import AuthHandler
from src.handlers.post_handler import PostHandler


@pytest.mark.requires_auth
@pytest.mark.integration
async def test_revert_approach():
    print("🔍 Testing simpler approach...")

    try:
        # Authenticate and create handlers
        auth = AuthHandler()
        client = await auth.authenticate()
        post_handler = PostHandler(client)

        # First, let's disable the new formatting approach temporarily
        # by testing with plain text only
        content = """# Test Without Formatting

This is a plain paragraph without any formatting.

## Another Section

Just plain text here too.

- Plain list item 1
- Plain list item 2
- Plain list item 3

No bold, no italic, no links. Just plain text."""

        print("📝 Creating plain text post...")

        create_result = await post_handler.create_draft(
            title="Plain Text Test",
            content=content,
            subtitle="Testing without formatting",
            content_type="markdown",
        )

        draft_id = create_result.get("id")
        print(f"✅ Draft created: {draft_id}")

        # Publish
        print("🚀 Publishing...")
        publish_result = await post_handler.publish_draft(draft_id)

        print(f"✅ Published!")
        slug = publish_result.get("slug")
        if slug:
            print(f"🔗 Post URL: https://neroaugustus.substack.com/p/{slug}")

        print("\n💡 If this works, the issue is with our formatted text handling!")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_revert_approach())
