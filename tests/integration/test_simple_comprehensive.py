#!/usr/bin/env python3
"""
Simple comprehensive test to verify content
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
async def test_simple_comprehensive():
    print("🧪 Testing simple comprehensive post...")

    try:
        # Authenticate and create handlers
        auth = AuthHandler()
        client = await auth.authenticate()
        post_handler = PostHandler(client)

        # Simple but comprehensive content
        content = """# Comprehensive Test - Simple

This post tests all major formatting options.

## Text Formatting

This is **bold text** and this is *italic text*. We can also have ***bold and italic*** combined.

Here's some `inline code` mixed with regular text.

## Headers Test

### H3 Header
#### H4 Header
##### H5 Header
###### H6 Header

## Lists

### Unordered List

• Item 1
• Item 2
• Item 3

### Ordered List

1. First item
2. Second item
3. Third item

## Code Blocks

### Python Code

```python
def hello_world():
    print("Hello, World!")
    return True

# Call the function
result = hello_world()
print(f"Result: {result}")
```

### JavaScript Code

```javascript
function greet(name) {
    console.log(`Hello, ${name}!`);
    return true;
}

// Call the function
const result = greet("World");
console.log(`Result: ${result}`);
```

## Blockquotes

> This is a simple blockquote.
> It can span multiple lines.

## Links and Images

Here's a [link to Substack](https://substack.com).

## Special Elements

---

Unicode test: 🎯 🚀 ✨ 💡 📝

## Conclusion

If you can see all the formatting above, the test is successful!"""

        print("📝 Creating comprehensive test post...")

        create_result = await post_handler.create_draft(
            title="✅ Simple Comprehensive Test",
            content=content,
            subtitle="Testing all major formatting options",
            content_type="markdown",
        )

        draft_id = create_result.get("id")
        print(f"✅ Draft created: {draft_id}")

        # Check the draft before publishing
        print("\n🔍 Checking draft content...")
        draft = client.get_draft(draft_id)
        if "draft_body" in draft:
            import json

            body_json = json.loads(draft["draft_body"])
            print(f"Draft has {len(body_json.get('content', []))} content blocks")

        # Publish
        print("\n🚀 Publishing...")
        publish_result = await post_handler.publish_draft(draft_id)

        print(f"✅ Published!")
        print(f"🌐 Post ID: {publish_result.get('id')}")

        slug = publish_result.get("slug")
        if slug:
            print(f"🔗 Post URL: https://neroaugustus.substack.com/p/{slug}")

        # Check published content
        if "body" in publish_result:
            body = publish_result["body"]
            if isinstance(body, str):
                body_json = json.loads(body)
                print(
                    f"\n✅ Published with {len(body_json.get('content', []))} content blocks"
                )

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_simple_comprehensive())
