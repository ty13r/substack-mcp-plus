#!/usr/bin/env python3
"""
Test if marks() is causing the issue
"""

import pytest
import sys
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.handlers.auth_handler import AuthHandler
from substack.post import Post

@pytest.mark.requires_auth
@pytest.mark.integration
async def test_marks_issue():
    print("🔍 Testing marks() behavior...")
    
    try:
        # Authenticate
        auth = AuthHandler()
        client = await auth.authenticate()
        user_id = client.get_user_id()
        
        # Test 1: Correct marks usage
        print("\n1️⃣ Correct marks usage...")
        post1 = Post(title="Correct Marks", subtitle="Should work", user_id=user_id)
        para1 = post1.paragraph()
        para1.text("Normal text ")
        para1.text("bold text")
        para1.marks([{"type": "strong"}])  # Only applies to "bold text"
        para1.text(" more normal")
        
        # Test 2: What we might be doing wrong
        print("\n2️⃣ Potentially wrong marks usage...")
        post2 = Post(title="Wrong Marks", subtitle="Might break", user_id=user_id)
        para2 = post2.paragraph()
        
        # If we call marks after text that shouldn't have marks
        para2.text("Normal text ")
        para2.marks([])  # Empty marks on normal text - might break?
        para2.text("bold text")
        para2.marks([{"type": "strong"}])
        para2.text(" more normal")
        para2.marks([])  # Empty marks again
        
        # Publish both
        draft1 = post1.get_draft()
        draft2 = post2.get_draft()
        
        id1 = client.post_draft(draft1)['id']
        id2 = client.post_draft(draft2)['id']
        
        pub1 = client.publish_draft(id1)
        pub2 = client.publish_draft(id2)
        
        print(f"\n✅ Correct: https://neroaugustus.substack.com/p/{pub1.get('slug')}")
        print(f"✅ Wrong: https://neroaugustus.substack.com/p/{pub2.get('slug')}")
        
        print("\n💡 If the second one is empty, we found the issue!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_marks_issue())