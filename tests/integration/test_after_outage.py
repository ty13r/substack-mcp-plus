#!/usr/bin/env python3
"""
Test after Substack outage is resolved
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
async def test_after_outage():
    print("🧪 Testing after Substack outage...")

    try:
        # Authenticate and create handlers
        auth = AuthHandler()
        client = await auth.authenticate()
        post_handler = PostHandler(client)

        # Create a simple test post
        content = """# Post-Outage Test

Substack is back online! Let's verify everything works.

## Test Content

This is a paragraph with **bold** and *italic* text.

- List item 1
- List item 2 with **formatting**

> A blockquote to test

Here's a [link](https://substack.com).

```python
def celebration():
    return "Substack is working again!"
```

Everything should display correctly now that Substack has resolved their issues."""

        print("📝 Creating test post...")

        create_result = await post_handler.create_draft(
            title="✅ Post-Outage Test",
            content=content,
            subtitle="Verifying everything works after Substack's recovery",
            content_type="markdown",
        )

        draft_id = create_result.get("id")
        print(f"✅ Draft created: {draft_id}")

        # Publish
        print("🚀 Publishing...")
        publish_result = await post_handler.publish_draft(draft_id)

        print(f"✅ Published!")
        print(f"🌐 Post ID: {publish_result.get('id')}")

        slug = publish_result.get("slug")
        if slug:
            print(f"🔗 Post URL: https://neroaugustus.substack.com/p/{slug}")

        print("\n🎯 Check if the content displays now that Substack is operational!")
        print(
            "\n📋 Also check our previous test posts - they should display content now too:"
        )
        print("   - https://neroaugustus.substack.com/p/reverted-handler-test")
        print("   - https://neroaugustus.substack.com/p/plain-text-test")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_after_outage())
