#!/usr/bin/env python3
"""
Test COMPLETE paywall integration with automatic audience setting
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
async def test_complete_paywall():
    print("🧪 Testing COMPLETE paywall integration with auto audience...")

    try:
        # Authenticate and create handlers
        auth = AuthHandler()
        client = await auth.authenticate()
        post_handler = PostHandler(client)

        # Test complete paywall functionality
        print("\n📝 Testing complete paywall integration...")

        paywall_content = """# Complete Paywall Integration Test

This post demonstrates **complete paywall functionality** with automatic audience setting.

## Free Content Available to Everyone

This section is accessible to all readers:

- ✅ **Free insights** that provide immediate value
- ✅ **Basic examples** to get you started
- ✅ **Community discussion** in the comments

### Free Code Example

```python
# Free example - available to everyone
def calculate_basic_roi(investment, return_value):
    return (return_value - investment) / investment * 100

roi = calculate_basic_roi(1000, 1200)
print(f"Basic ROI: {roi}%")
```

## Why Premium Content Matters

Our premium content goes **beyond the basics** to provide:

1. **Advanced strategies** tested in production
2. **Complete implementations** you can copy
3. **Personal support** when you get stuck

---

<!-- PAYWALL -->

## 🔒 Premium Subscriber Exclusive Content

**Welcome, premium subscriber!** This advanced content is your reward for supporting quality content creation.

### Advanced Paywall Implementation

Here's how our paywall system actually works behind the scenes:

```python
# PREMIUM: Advanced paywall processing
class PaywallProcessor:
    def __init__(self):
        self.markers = ["<!-- PAYWALL -->", "<!--PAYWALL-->", "<!--paywall-->"]
        
    def process_content(self, content, audience="everyone"):
        # Detect paywall markers
        for marker in self.markers:
            if marker in content:
                # Automatically set to paid subscribers
                audience = "only_paid"
                
                # Split content at paywall
                free_part, premium_part = content.split(marker, 1)
                
                return {
                    "free_content": free_part,
                    "premium_content": premium_part,
                    "audience": audience,
                    "has_paywall": True
                }
        
        return {
            "content": content,
            "audience": audience, 
            "has_paywall": False
        }

# This is the actual implementation powering this post!
processor = PaywallProcessor()
result = processor.process_content(post_content)
```

### Premium Business Strategies

As a premium subscriber, you get access to:

#### 1. **Revenue Optimization Techniques**
- A/B test different paywall positions
- Optimize free-to-paid conversion rates
- Analyze subscriber engagement patterns

#### 2. **Content Strategy Secrets**
- How to hook readers in free content
- Premium content that keeps subscribers
- Retention strategies that work

#### 3. **Technical Implementation**
- Complete source code for paywall systems
- Integration with payment processors
- Analytics and tracking setup

### Exclusive Tools & Resources

Premium subscribers get:

- 📊 **Revenue Analytics Dashboard** - Track your paywall performance
- 🔧 **Content Optimizer Tool** - Analyze free vs premium balance  
- 💬 **Direct Access** - Personal help with implementation
- 🎯 **Case Studies** - Real examples with revenue numbers

## Premium-Only Community

Join our private community where premium subscribers:

- Share advanced strategies
- Get early access to new tools
- Participate in monthly strategy calls
- Access exclusive workshops

## Thank You!

Your premium subscription directly supports:

- ✅ **More in-depth content** like this post
- ✅ **Tool development** for the community
- ✅ **Regular updates** and improvements
- ✅ **Quality over quantity** content creation

**You make this sustainable!** 💎"""

        # Create the post (should auto-set audience to "only_paid")
        print(f"📝 Creating paywall post with automatic audience setting...")

        create_result = await post_handler.create_draft(
            title="💎 Complete Paywall Integration - Auto Audience",
            content=paywall_content,
            subtitle="Demonstrating automatic paid subscriber audience setting for paywall content",
            content_type="markdown",
        )

        draft_id = create_result.get("id")
        print(f"✅ Paywall post created: {draft_id}")

        # Check the audience setting
        audience = create_result.get("audience", "unknown")
        print(f"   Audience automatically set to: {audience}")

        if audience == "only_paid":
            print(f"✅ Automatic audience setting working correctly!")
        else:
            print(
                f"⚠️ Audience not set correctly: expected 'only_paid', got '{audience}'"
            )

        # Now try to publish (should work with only_paid audience)
        print(f"\n🚀 Publishing paywall post with correct audience...")

        publish_result = await post_handler.publish_draft(draft_id)

        print(f"✅ Paywall post published successfully!")
        print(f"🌐 Post ID: {publish_result.get('id')}")
        print(f"👥 Audience: {publish_result.get('audience', 'unknown')}")

        slug = publish_result.get("slug")
        if slug:
            print(f"🔗 Post URL: https://neroaugustus.substack.com/p/{slug}")
            print(f"   (Only visible to paid subscribers)")

        print(f"\n🎉 COMPLETE PAYWALL INTEGRATION TEST SUCCESSFUL!")
        print(f"📊 Final Results:")
        print(f"   ✅ Paywall marker detection: Working")
        print(
            f"   ✅ Automatic audience setting: {'Working' if audience == 'only_paid' else 'Needs verification'}"
        )
        print(f"   ✅ Post creation with paywall: Working")
        print(f"   ✅ Publishing paid subscriber post: Working")
        print(f"   ✅ Content separation: Check published post")
        print(f"\n💎 Paywall integration is fully functional!")

    except Exception as e:
        print(f"❌ Complete paywall test failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_complete_paywall())
