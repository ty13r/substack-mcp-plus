#!/usr/bin/env python3
"""
Test the fixed post creation with proper python-substack library usage
"""

import pytest
import sys
import os
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.handlers.auth_handler import AuthHandler
from src.handlers.post_handler import PostHandler


@pytest.mark.requires_auth
@pytest.mark.integration
async def test_fixed_post():
    """Test the fixed post creation"""

    # Authenticate
    auth_handler = AuthHandler()
    client = await auth_handler.authenticate()

    # Simple test content
    content = """# Fixed Post Test

This is a **bold** test of the fixed implementation.

Here's a *italic* paragraph with `inline code`.

## Subheader Works

- List item 1
- List item 2  
- List item 3

```python
def test():
    print("Code block test")
```

> This is a blockquote test

---

Content after horizontal rule."""

    # Create the post handler
    post_handler = PostHandler(client)

    print("Creating fixed test post...")

    try:
        # Create the draft
        result = await post_handler.create_draft(
            title="🔧 Fixed Implementation Test",
            content=content,
            subtitle="Testing the corrected python-substack integration",
            content_type="markdown",
        )

        draft_id = result.get("id")
        print(f"✅ Draft created successfully!")
        print(f"📝 Draft ID: {draft_id}")

        # Publish immediately
        publish_result = await post_handler.publish_draft(draft_id)

        print(f"✅ Post published successfully!")
        print(f"🌐 Post ID: {publish_result.get('id')}")

        # Get the slug for URL
        slug = publish_result.get("slug")
        if slug:
            print(f"🔗 Post URL: https://neroaugustus.substack.com/p/{slug}")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_fixed_post())
