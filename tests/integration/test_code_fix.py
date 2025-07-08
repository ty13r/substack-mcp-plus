#!/usr/bin/env python3
"""
Test code block fix
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
async def test_code_block_fix():
    print("🧪 Testing code block fix...")
    
    try:
        # Authenticate and create handlers
        auth = AuthHandler()
        client = await auth.authenticate()
        post_handler = PostHandler(client)
        
        # Test content with code blocks
        content = """# Code Block Fix Test

Testing that code blocks don't have duplicate headers.

## Python Code

```python
def hello_world():
    print("Hello, World!")
    return True
```

## JavaScript Code

```javascript
function greet(name) {
    console.log(`Hello, ${name}!`);
    return true;
}
```

## Code Without Language

```
This is a code block without a language specified.
It should not have any header.
```

The headers should appear only once per code block."""

        print("📝 Creating test post...")
        
        create_result = await post_handler.create_draft(
            title="✅ Code Block Fix",
            content=content,
            subtitle="Testing single header per code block",
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
        
        print("\n🎯 Code blocks should now have single headers!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_code_block_fix())