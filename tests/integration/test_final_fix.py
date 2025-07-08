#!/usr/bin/env python3
"""
Test if the fix works
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
async def test_final_fix():
    print("🧪 Testing final fix...")

    try:
        # Authenticate and create handlers
        auth = AuthHandler()
        client = await auth.authenticate()
        post_handler = PostHandler(client)

        # Test content with formatting
        content = """# Final Fix Test

This is a paragraph with **bold** and *italic* text.

## Working Now?

- Item with **bold**
- Item with *italic*  
- Regular item

> Blockquote with **formatting**

Here's a [link](https://substack.com).

```python
def success():
    return "It works!"
```

🎉 All formatting should display correctly now!"""

        print("📝 Creating test post...")

        create_result = await post_handler.create_draft(
            title="🎉 Final Fix Test - Should Work!",
            content=content,
            subtitle="Testing the marks() fix",
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

        print("\n🤞 Check if content displays now!")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_final_fix())
