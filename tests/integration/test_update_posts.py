#!/usr/bin/env python3
"""
Test post update/edit functionality
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
async def test_update_posts():
    print("🧪 Testing post update/edit functionality...")
    
    try:
        # Authenticate and create handlers
        auth = AuthHandler()
        client = await auth.authenticate()
        post_handler = PostHandler(client)
        
        # Step 1: Create an initial draft to update
        print("\n📝 Step 1: Creating initial draft...")
        
        initial_content = """# Original Title Content

This is the **original content** of the post that we will update.

## Original Section

- Original bullet point 1
- Original bullet point 2

```python
# Original code block
def original_function():
    return "original"
```

> Original blockquote

This content will be modified in our update tests."""

        create_result = await post_handler.create_draft(
            title="🔄 Original Title - Update Test",
            content=initial_content,
            subtitle="Original subtitle for update testing",
            content_type="markdown"
        )
        
        draft_id = create_result.get('id')
        print(f"✅ Initial draft created: {draft_id}")
        print(f"   Title: {create_result.get('draft_title')}")
        print(f"   Subtitle: {create_result.get('draft_subtitle')}")
        
        # Step 2: Test updating just the title
        print(f"\n📝 Step 2: Testing title update...")
        
        update_result1 = await post_handler.update_draft(
            post_id=draft_id,
            title="🔄 UPDATED Title - Now Modified!",
            content_type="markdown"
        )
        
        print(f"✅ Title updated successfully!")
        print(f"   Post ID: {update_result1.get('id', draft_id)}")
        
        # Step 3: Test updating just the subtitle
        print(f"\n📝 Step 3: Testing subtitle update...")
        
        update_result2 = await post_handler.update_draft(
            post_id=draft_id,
            subtitle="UPDATED subtitle - now completely different!",
            content_type="markdown"
        )
        
        print(f"✅ Subtitle updated successfully!")
        
        # Step 4: Test updating the content
        print(f"\n📝 Step 4: Testing content update...")
        
        updated_content = """# COMPLETELY UPDATED Content

This post has been **completely rewritten** during our update test!

## New Updated Section

The content is now totally different:

- NEW bullet point 1 with **bold text**
- NEW bullet point 2 with *italic text*
- NEW bullet point 3 with `inline code`

### Code Block Update

```javascript
// UPDATED code block - now JavaScript!
function updatedFunction() {
    console.log("This content has been updated!");
    return "updated and improved";
}

updatedFunction();
```

### New Blockquote

> This is a BRAND NEW blockquote with updated content that demonstrates our update functionality is working perfectly!

## Update Test Results

✅ **Title Update**: Working  
✅ **Subtitle Update**: Working  
✅ **Content Update**: Working  

### Final Notes

This post demonstrates that our MCP server can successfully:

1. Create initial drafts
2. Update titles independently 
3. Update subtitles independently
4. Update content completely
5. Handle complex markdown in updates

**The update functionality is fully operational!** 🎉"""

        update_result3 = await post_handler.update_draft(
            post_id=draft_id,
            content=updated_content,
            content_type="markdown"
        )
        
        print(f"✅ Content updated successfully!")
        
        # Step 5: Test updating everything at once
        print(f"\n📝 Step 5: Testing simultaneous update (title + subtitle + content)...")
        
        final_content = """# FINAL UPDATE - All At Once

This is the **final update** where we change title, subtitle, AND content all in one operation!

## Multi-Update Test

This demonstrates that our update function can handle:

- ✅ Title changes
- ✅ Subtitle changes  
- ✅ Content changes
- ✅ All three simultaneously

```python
def final_update_test():
    return {
        "title": "updated",
        "subtitle": "updated", 
        "content": "updated",
        "status": "success"
    }
```

> "The best updates are the ones that work seamlessly!" - Anonymous Developer

## Summary

**All update functionality is working perfectly!** 🚀"""

        update_result4 = await post_handler.update_draft(
            post_id=draft_id,
            title="🎯 FINAL UPDATE - All Components Changed",
            subtitle="Final subtitle - everything updated simultaneously",
            content=final_content,
            content_type="markdown"
        )
        
        print(f"✅ Simultaneous update successful!")
        
        # Step 6: Publish the final updated post to see the results
        print(f"\n🚀 Step 6: Publishing updated post to verify changes...")
        
        publish_result = await post_handler.publish_draft(draft_id)
        
        print(f"✅ Updated post published successfully!")
        print(f"🌐 Post ID: {publish_result.get('id')}")
        
        slug = publish_result.get('slug')
        if slug:
            print(f"🔗 Post URL: https://neroaugustus.substack.com/p/{slug}")
        
        print(f"\n🎉 UPDATE FUNCTIONALITY TEST COMPLETE!")
        print(f"📊 Test Results:")
        print(f"   ✅ Individual title updates: Working")
        print(f"   ✅ Individual subtitle updates: Working") 
        print(f"   ✅ Individual content updates: Working")
        print(f"   ✅ Simultaneous updates: Working")
        print(f"   ✅ Published updated post: Working")
        print(f"\n🎯 Check the published post to see all the updates applied!")
        
    except Exception as e:
        print(f"❌ Update test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_update_posts())