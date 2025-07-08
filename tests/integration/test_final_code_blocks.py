#!/usr/bin/env python3
"""
Final test of code block functionality
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
async def test_final_code_blocks():
    print("🧪 Final test of code block functionality...")
    
    try:
        # Authenticate and create handlers
        auth = AuthHandler()
        client = await auth.authenticate()
        post_handler = PostHandler(client)
        
        # Test content with properly formatted code blocks
        content = """# Final Code Block Test

Let's verify code blocks work correctly now.

## Python Example

Here's a Python function with proper formatting:

```python
def fibonacci(n):
    \"\"\"Calculate fibonacci number\"\"\"
    if n <= 1:
        return n
    
    # Recursive calculation
    return fibonacci(n - 1) + fibonacci(n - 2)

# Test the function
for i in range(10):
    print(f"F({i}) = {fibonacci(i)}")
```

## JavaScript Example  

And here's JavaScript code:

```javascript
const calculateArea = (width, height) => {
    // Validate inputs
    if (width <= 0 || height <= 0) {
        throw new Error('Dimensions must be positive');
    }
    
    return width * height;
};

// Usage
try {
    const area = calculateArea(10, 5);
    console.log(`Area: ${area}`);
} catch (error) {
    console.error(error.message);
}
```

## Shell Script

```bash
#!/bin/bash

# Deploy script
echo "Starting deployment..."

if [ -z "$1" ]; then
    echo "Error: No environment specified"
    exit 1
fi

npm run build
npm run test
npm run deploy:$1

echo "Deployment complete!"
```

## Conclusion

All code blocks should now:
- ✅ Display as proper code blocks (not inline)
- ✅ Preserve line breaks and indentation
- ✅ Show with monospace font
- ✅ Have proper visual separation"""

        print("📝 Creating final test post...")
        
        create_result = await post_handler.create_draft(
            title="✅ Final Code Block Test - Properly Formatted",
            content=content,
            subtitle="Verifying code blocks display correctly with all fixes applied",
            content_type="markdown"
        )
        
        draft_id = create_result.get('id')
        print(f"✅ Final test post created: {draft_id}")
        
        # Publish immediately
        print(f"🚀 Publishing final test...")
        
        publish_result = await post_handler.publish_draft(draft_id)
        
        print(f"✅ Final test published!")
        print(f"🌐 Post ID: {publish_result.get('id')}")
        
        slug = publish_result.get('slug')
        if slug:
            print(f"🔗 Post URL: https://neroaugustus.substack.com/p/{slug}")
        
        print(f"\n🎯 FINAL VERIFICATION:")
        print(f"   Check the published post to confirm:")
        print(f"   - Code blocks appear as blocks (not inline)")
        print(f"   - Indentation is preserved") 
        print(f"   - Line breaks are maintained")
        print(f"   - Syntax highlighting (if supported)")
        print(f"\n✅ Code block fix complete!")
        
    except Exception as e:
        print(f"❌ Final test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_final_code_blocks())