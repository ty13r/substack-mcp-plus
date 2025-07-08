#!/usr/bin/env python3
"""
Compare working vs not working posts
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
async def test_direct_comparison():
    print("🔍 Comparing different post creation methods...")

    try:
        # Authenticate
        auth = AuthHandler()
        client = await auth.authenticate()
        user_id = client.get_user_id()

        # Method 1: Direct Post object (this was working before)
        print("\n1️⃣ Method 1: Direct Post object...")
        post1 = Post(
            title="Direct Post Test",
            subtitle="Using Post object directly",
            user_id=user_id,
        )

        post1.paragraph("This is a test paragraph.")
        post1.heading("Test Heading", 2)
        post1.paragraph("Another paragraph.")

        draft_data1 = post1.get_draft()
        result1 = client.post_draft(draft_data1)
        pub1 = client.publish_draft(result1["id"])

        print(f"✅ Published: {result1['id']}")
        print(f"   Body exists: {'body' in pub1}")
        print(f"   URL: https://neroaugustus.substack.com/p/{pub1.get('slug')}")

        # Let's check what's different about posts that were working
        print("\n2️⃣ Checking a working post (from earlier)...")
        # The test that worked had ID 167618884
        working_post_id = "167618884"
        try:
            working_post = client.get_draft(working_post_id)
            print(f"Working post type: {working_post.get('type')}")
            print(f"Working post editor_v2: {working_post.get('editor_v2')}")

            # Compare with our new post
            new_post = client.get_draft(result1["id"])
            print(f"\nNew post type: {new_post.get('type')}")
            print(f"New post editor_v2: {new_post.get('editor_v2')}")

            # Check for any differences
            print("\n📊 Key differences:")
            for key in ["editor_v2", "type", "is_published"]:
                if working_post.get(key) != new_post.get(key):
                    print(f"  {key}: {working_post.get(key)} -> {new_post.get(key)}")

        except Exception as e:
            print(f"Could not fetch working post: {e}")

        # Method 3: Check if we need to set editor_v2
        print("\n3️⃣ Testing with editor_v2 flag...")
        post3 = Post(
            title="Editor V2 Test", subtitle="Testing with editor flag", user_id=user_id
        )

        # Add content
        post3.paragraph("Testing editor v2 flag.")

        # Get draft and modify
        draft_data3 = post3.get_draft()
        draft_data3["editor_v2"] = True  # Force editor v2

        result3 = client.post_draft(draft_data3)
        pub3 = client.publish_draft(result3["id"])

        print(f"✅ Published with editor_v2: {result3['id']}")
        print(f"   URL: https://neroaugustus.substack.com/p/{pub3.get('slug')}")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_direct_comparison())
