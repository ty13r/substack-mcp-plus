#!/usr/bin/env python3
"""
Test with reverted PostHandler
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
async def test_reverted_posthandler():
    print("🧪 Testing with reverted PostHandler...")

    try:
        # Authenticate and create handlers
        auth = AuthHandler()
        client = await auth.authenticate()
        post_handler = PostHandler(client)

        # Test content with formatting
        content = """# Reverted PostHandler Test

This is a paragraph with **bold** and *italic* text.

## Lists

- Item with **bold**
- Item with *italic*
- Regular item

## Blockquotes

> This is a blockquote.
> It should display properly now.

## Links

Here's a [link to Substack](https://substack.com).

## Code

```python
def working():
    return "Should work now!"
```

The content should display correctly with the simpler approach."""

        print("📝 Creating test post with reverted handler...")

        create_result = await post_handler.create_draft(
            title="✅ Reverted Handler Test",
            content=content,
            subtitle="Back to simpler approach",
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

        print("\n🎯 The simpler approach should work!")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_reverted_posthandler())
