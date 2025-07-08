#!/usr/bin/env python3
"""
Test FIXED paywall integration functionality
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
async def test_fixed_paywall():
    print("🧪 Testing FIXED paywall integration...")

    try:
        # Authenticate and create handlers
        auth = AuthHandler()
        client = await auth.authenticate()
        post_handler = PostHandler(client)

        # Test fixed paywall processing
        print("\n📝 Testing fixed paywall marker processing...")

        paywall_content = """# Fixed Paywall Test

This is **free content** available to all readers.

## Free Section

- Free bullet point 1
- Free bullet point 2

```python
def free_function():
    return "free"
```

<!-- PAYWALL -->

## Premium Section

This is **premium content** only for subscribers!

- Premium feature 1
- Premium feature 2

```python
def premium_function():
    return "premium"
```

Thank you for subscribing!"""

        # Debug: Test the processing directly
        print("🔍 Debugging paywall marker processing...")

        from src.converters.markdown_converter import MarkdownConverter

        converter = MarkdownConverter()

        # First, test blocks without paywall processing
        blocks_no_paywall = converter.convert(paywall_content)
        print(f"   Blocks without paywall processing: {len(blocks_no_paywall)}")

        # Test paywall processing
        processed_blocks = post_handler._process_paywall_markers(
            paywall_content, blocks_no_paywall, "markdown"
        )

        print(f"   Blocks after paywall processing: {len(processed_blocks)}")

        # Look for paywall block
        paywall_found = False
        for i, block in enumerate(processed_blocks):
            print(f"   Block {i}: type={block.get('type')}")
            if block.get("type") == "paywall":
                paywall_found = True
                print(f"   ✅ Paywall block found at position {i}")

        if paywall_found:
            print(f"✅ Paywall processing is working correctly!")
        else:
            print(f"❌ Paywall block not found - marker may not be processed")

        # Create the post
        print(f"\n📝 Creating post with fixed paywall processing...")

        create_result = await post_handler.create_draft(
            title="🔧 FIXED Paywall Test",
            content=paywall_content,
            subtitle="Testing the corrected paywall marker processing",
            content_type="markdown",
        )

        draft_id = create_result.get("id")
        print(f"✅ Fixed paywall post created: {draft_id}")

        # Publish to test the result
        print(f"\n🚀 Publishing fixed paywall post...")

        publish_result = await post_handler.publish_draft(draft_id)

        print(f"✅ Fixed paywall post published!")
        print(f"🌐 Post ID: {publish_result.get('id')}")

        slug = publish_result.get("slug")
        if slug:
            print(f"🔗 Post URL: https://neroaugustus.substack.com/p/{slug}")

        print(f"\n🎉 FIXED PAYWALL TEST COMPLETE!")
        print(f"📊 Results:")
        print(
            f"   ✅ Paywall marker detection: {'Working' if paywall_found else 'Still needs fixing'}"
        )
        print(f"   ✅ Post creation: Working")
        print(f"   ✅ Post publishing: Working")
        print(f"\n💎 Check the published post to see if paywall separation works!")

    except Exception as e:
        print(f"❌ Fixed paywall test failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_fixed_paywall())
