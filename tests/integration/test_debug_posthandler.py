#!/usr/bin/env python3
"""
Debug what PostHandler is doing differently
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
from src.handlers.post_handler import PostHandler
from substack.post import Post


async def debug_posthandler():
    print("🔍 Debugging PostHandler vs direct Post object...")

    try:
        # Authenticate
        auth = AuthHandler()
        client = await auth.authenticate()
        user_id = client.get_user_id()

        # Test 1: Direct Post object (WORKING)
        print("\n1️⃣ Direct Post object (WORKING)...")
        post1 = Post(
            title="Direct Post - Working", subtitle="This should work", user_id=user_id
        )

        post1.paragraph("This is a simple paragraph.")
        post1.heading("Test Heading", 2)
        post1.paragraph("Another paragraph.")

        draft1 = post1.get_draft()
        body1 = json.loads(draft1["draft_body"])
        print(f"Direct Post blocks: {len(body1['content'])}")
        print(f"First block: {json.dumps(body1['content'][0], indent=2)}")

        # Test 2: PostHandler (NOT WORKING)
        print("\n2️⃣ PostHandler method...")
        post_handler = PostHandler(client)

        markdown = """This is a simple paragraph.

## Test Heading

Another paragraph."""

        # Create using PostHandler
        result = await post_handler.create_draft(
            title="PostHandler - Debug",
            content=markdown,
            subtitle="Why doesn't this work?",
            content_type="markdown",
        )

        # Get the created draft
        draft2 = client.get_draft(result["id"])
        body2_str = draft2.get("draft_body", "{}")
        body2 = json.loads(body2_str)
        print(f"\nPostHandler blocks: {len(body2['content'])}")
        print(f"First block: {json.dumps(body2['content'][0], indent=2)}")

        # Compare the structures
        print("\n3️⃣ Comparing structures...")

        # Publish both
        pub1 = client.publish_draft(client.post_draft(draft1)["id"])
        pub2 = client.publish_draft(result["id"])

        print(
            f"\n✅ Direct Post published: https://neroaugustus.substack.com/p/{pub1.get('slug')}"
        )
        print(
            f"✅ PostHandler published: https://neroaugustus.substack.com/p/{pub2.get('slug')}"
        )

        # Check what's in the published versions
        print("\n4️⃣ Checking published content...")

        pub1_body = pub1.get("body")
        pub2_body = pub2.get("body")

        if pub1_body and pub2_body:
            p1_parsed = json.loads(pub1_body)
            p2_parsed = json.loads(pub2_body)

            print(f"Direct Post published blocks: {len(p1_parsed.get('content', []))}")
            print(f"PostHandler published blocks: {len(p2_parsed.get('content', []))}")

            # Show first block of each
            if p1_parsed.get("content"):
                print(
                    f"\nDirect first block type: {p1_parsed['content'][0].get('type')}"
                )
            if p2_parsed.get("content"):
                print(
                    f"PostHandler first block type: {p2_parsed['content'][0].get('type')}"
                )

    except Exception as e:
        print(f"❌ Debug failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(debug_posthandler())
