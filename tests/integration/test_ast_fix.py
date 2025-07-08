#!/usr/bin/env python3
"""
Test the AST text extraction fix
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
async def test_ast_fix():
    """Test the AST text extraction fix"""

    # Authenticate
    auth_handler = AuthHandler()
    client = await auth_handler.authenticate()

    # Simple test content with formatting
    content = """# AST Fix Test

This is a **bold** test with *italic* text and `inline code`.

Here's a [link](https://example.com) in a paragraph.

> This is a blockquote to test if quotes work

## List Test

- Bullet point one
- Bullet point two

1. Numbered item one
2. Numbered item two

```javascript
function test() { return "code test"; }
```

---

Final paragraph after horizontal rule."""

    # Create the post handler
    post_handler = PostHandler(client)

    print("Testing AST text extraction fix...")

    try:
        # Create the draft
        result = await post_handler.create_draft(
            title="AST Text Extraction Fix Test",
            content=content,
            subtitle="Testing if text is properly extracted from AST",
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

        print(f"\n🎯 Check the post to see if text renders properly instead of AST!")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_ast_fix())
