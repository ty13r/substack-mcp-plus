#!/usr/bin/env python3
"""
Test with the fix applied
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
async def test_fixed_formatting():
    print("🧪 Testing with fix applied...")

    try:
        # Authenticate and create handlers
        auth = AuthHandler()
        client = await auth.authenticate()
        post_handler = PostHandler(client)

        # Test content
        content = """# Fixed Formatting Test

This is a paragraph with **bold** and *italic* text.

## Lists

- Item with **bold**
- Item with *italic*
- Item with `code`

## Blockquotes

> This is a blockquote with **formatting**.

## Links

Here's a [link to Substack](https://substack.com).

## Code

```python
def test():
    return "Working!"
```

All formatting should work now!"""

        print("📝 Creating test post...")

        create_result = await post_handler.create_draft(
            title="✅ Fixed Formatting Test",
            content=content,
            subtitle="All formatting should work now",
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

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_fixed_formatting())
