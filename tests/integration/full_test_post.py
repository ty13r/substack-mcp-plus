#!/usr/bin/env python3
"""
Create and publish a comprehensive test post with all markdown formatting types
"""

import sys
import os
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.handlers.auth_handler import AuthHandler
from src.handlers.post_handler import PostHandler


async def create_comprehensive_test_post():
    """Create a comprehensive test post with all formatting types"""

    # Authenticate
    auth_handler = AuthHandler()
    client = await auth_handler.authenticate()

    # Create comprehensive test content
    content = """# Comprehensive Markdown Test Post

Welcome to this **comprehensive test** of all markdown formatting features available in our Substack MCP Plus server!

## Text Formatting

Here we test various text formatting options:

- **Bold text** using double asterisks
- *Italic text* using single asterisks  
- ***Bold and italic*** using triple asterisks
- `Inline code` using backticks
- Regular text without any formatting

## Headers

We support all header levels:

### Header Level 3
#### Header Level 4
##### Header Level 5
###### Header Level 6

## Lists

### Unordered Lists

- First item in unordered list
- Second item with **bold text**
- Third item with *italic text*
- Fourth item with `inline code`

### Ordered Lists

1. First numbered item
2. Second numbered item with **formatting**
3. Third numbered item
4. Fourth numbered item

### Nested Lists

- Main item 1
  - Sub item 1.1
  - Sub item 1.2
- Main item 2
  - Sub item 2.1
  - Sub item 2.2

## Code Blocks

Here's a Python code block:

```python
def hello_world():
    print("Hello from Substack MCP Plus!")
    
    # This is a comment
    numbers = [1, 2, 3, 4, 5]
    
    for num in numbers:
        if num % 2 == 0:
            print(f"{num} is even")
        else:
            print(f"{num} is odd")

hello_world()
```

Here's a JavaScript code block:

```javascript
function fibonacci(n) {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

// Generate first 10 fibonacci numbers
for (let i = 0; i < 10; i++) {
    console.log(`F(${i}) = ${fibonacci(i)}`);
}
```

## Blockquotes

> This is a simple blockquote. It should appear with special formatting to distinguish it from regular text.

> This is a longer blockquote that spans multiple sentences. It demonstrates how longer quoted content should appear. The formatting should remain consistent across the entire quote.

## Links

Here are some test links:

- [OpenAI](https://openai.com) - Link to OpenAI
- [Substack](https://substack.com) - Link to Substack
- [GitHub](https://github.com) - Link to GitHub

## Horizontal Rules

Here's a horizontal rule:

---

Content after the horizontal rule.

## Mixed Formatting

This paragraph contains **bold text**, *italic text*, `inline code`, and a [link to example.com](https://example.com) all in one sentence to test mixed formatting.

## Free vs Paid Content

This content is available to all readers.

<!-- PAYWALL -->

This content appears after the paywall marker and should only be visible to paid subscribers.

### Paid Subscriber Benefits

- Access to exclusive content
- Early access to new posts  
- Community discussion access
- Direct author interaction

## Conclusion

This comprehensive test post demonstrates all the markdown formatting capabilities of our Substack MCP Plus server:

1. ✅ Headers (H1-H6)
2. ✅ Text formatting (bold, italic, code)
3. ✅ Lists (ordered, unordered, nested)
4. ✅ Code blocks with syntax highlighting
5. ✅ Blockquotes
6. ✅ Links
7. ✅ Horizontal rules
8. ✅ Mixed formatting
9. ✅ Paywall integration

**Thank you for testing our Substack MCP Plus server!** 🚀"""

    # Create the post handler
    post_handler = PostHandler(client)

    print("Creating comprehensive test post...")

    try:
        # Create the draft
        result = await post_handler.create_draft(
            title="🧪 Comprehensive Markdown Test - All Formatting Types",
            content=content,
            subtitle="Testing every markdown feature supported by Substack MCP Plus",
            content_type="markdown",
        )

        draft_id = result.get("id")
        print(f"✅ Draft created successfully!")
        print(f"📝 Draft ID: {draft_id}")
        print(f"📋 Title: {result.get('draft_title', 'Unknown')}")

        # Publish the draft immediately
        print(f"\n🚀 Publishing draft {draft_id}...")

        publish_result = await post_handler.publish_draft(draft_id)

        print(f"✅ Post published successfully!")
        print(f"🌐 Post ID: {publish_result.get('id')}")
        print(f"📅 Published at: {publish_result.get('post_date')}")
        print(f"📧 Email sent at: {publish_result.get('email_sent_at')}")

        # Get the slug for the URL
        slug = publish_result.get("slug")
        if slug:
            print(f"🔗 Post URL: https://neroaugustus.substack.com/p/{slug}")

        print(
            f"\n🎉 Check your Substack publication to see all the formatting in action!"
        )

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(create_comprehensive_test_post())
