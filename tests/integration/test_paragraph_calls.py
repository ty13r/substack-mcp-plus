#!/usr/bin/env python3
"""
Test different ways of calling paragraph
"""

import pytest
import sys
import os
import asyncio
import json
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.handlers.auth_handler import AuthHandler
from substack.post import Post


@pytest.mark.requires_auth
@pytest.mark.integration
async def test_paragraph_calls():
    print("🔍 Testing different paragraph call methods...")

    try:
        # Authenticate
        auth = AuthHandler()
        client = await auth.authenticate()
        user_id = client.get_user_id()

        # Method 1: Simple paragraph (WORKING)
        print("\n1️⃣ Method 1: Simple paragraph call...")
        post1 = Post(title="Method 1", subtitle="Simple", user_id=user_id)
        post1.paragraph("This works fine.")

        draft1 = post1.get_draft()
        print(f"Method 1 draft_body length: {len(draft1['draft_body'])}")

        # Method 2: Paragraph with chained text calls
        print("\n2️⃣ Method 2: Chained text calls...")
        post2 = Post(title="Method 2", subtitle="Chained", user_id=user_id)
        para = post2.paragraph()
        para.text("This is ")
        para.text("bold")
        para.marks([{"type": "strong"}])
        para.text(" text.")

        draft2 = post2.get_draft()
        print(f"Method 2 draft_body length: {len(draft2['draft_body'])}")

        # Method 3: What our PostHandler does
        print("\n3️⃣ Method 3: Our PostHandler approach...")
        post3 = Post(title="Method 3", subtitle="PostHandler style", user_id=user_id)
        para = post3.paragraph()

        # Simulate what _add_formatted_content_to_paragraph does
        content = [
            {"type": "text", "content": "This is "},
            {"type": "text", "content": "bold", "marks": [{"type": "strong"}]},
            {"type": "text", "content": " text."},
        ]

        for item in content:
            text = item.get("content", item.get("text", ""))
            marks = item.get("marks", [])

            para.text(text)
            if marks:
                para.marks(marks)

        draft3 = post3.get_draft()
        print(f"Method 3 draft_body length: {len(draft3['draft_body'])}")

        # Publish all three
        print("\n📤 Publishing all three...")

        id1 = client.post_draft(draft1)["id"]
        id2 = client.post_draft(draft2)["id"]
        id3 = client.post_draft(draft3)["id"]

        pub1 = client.publish_draft(id1)
        pub2 = client.publish_draft(id2)
        pub3 = client.publish_draft(id3)

        print(f"\n✅ Method 1: https://neroaugustus.substack.com/p/{pub1.get('slug')}")
        print(f"✅ Method 2: https://neroaugustus.substack.com/p/{pub2.get('slug')}")
        print(f"✅ Method 3: https://neroaugustus.substack.com/p/{pub3.get('slug')}")

        # Check the actual content structure
        print("\n📊 Checking content structures...")
        for i, draft in enumerate([draft1, draft2, draft3], 1):
            body = json.loads(draft["draft_body"])
            first_para = body["content"][0]
            print(f"\nMethod {i} paragraph content:")
            print(json.dumps(first_para["content"], indent=2))

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_paragraph_calls())
