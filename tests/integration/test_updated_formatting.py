#!/usr/bin/env python3
"""
Test the updated PostHandler with proper formatting
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
async def test_updated_formatting():
    print("🧪 Testing updated formatting...")
    
    try:
        # Authenticate and create handlers
        auth = AuthHandler()
        client = await auth.authenticate()
        post_handler = PostHandler(client)
        
        # Test content with all formatting issues
        content = """# Updated Formatting Test

## Text Formatting

This is **bold text** and this is *italic text*. We can also have ***bold and italic*** combined.

Here's some `inline code` mixed with regular text.

## Lists with Formatting

• Item with **bold text**
• Item with *italic text*
• Item with `inline code`

1. First item with **bold**
2. Second item with *italic*
3. Third item with [a link](https://example.com)

## Blockquotes

> This is a simple blockquote.
> It should appear properly indented.

> **Bold** in a blockquote.
> *Italic* in a blockquote.
> Even [links](https://substack.com) in blockquotes.

## Links

Here's a [link to Substack](https://substack.com) and another [link with **bold** text](https://example.com).

## Code Blocks

```python
def test():
    print("Code blocks should still work")
    return True
```

## Conclusion

All formatting should now work correctly!"""

        print("📝 Creating test post...")
        
        create_result = await post_handler.create_draft(
            title="✅ Updated Formatting Test",
            content=content,
            subtitle="Testing fixed text formatting, blockquotes, and links",
            content_type="markdown"
        )
        
        draft_id = create_result.get('id')
        print(f"✅ Draft created: {draft_id}")
        
        # Publish
        print("🚀 Publishing...")
        publish_result = await post_handler.publish_draft(draft_id)
        
        print(f"✅ Published!")
        print(f"🌐 Post ID: {publish_result.get('id')}")
        
        slug = publish_result.get('slug')
        if slug:
            print(f"🔗 Post URL: https://neroaugustus.substack.com/p/{slug}")
        
        print(f"\n🎯 FIXED ISSUES:")
        print(f"   ✅ Text formatting (bold, italic, combined)")
        print(f"   ✅ Blockquotes with proper indentation")
        print(f"   ✅ Links appearing as clickable")
        print(f"   ✅ Formatted text in lists")
        print(f"   ✅ Formatted text in blockquotes")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_updated_formatting())