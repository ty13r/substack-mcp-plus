#!/usr/bin/env python3
"""
Debug why content isn't appearing in posts
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


async def debug_content_issue():
    print("🔍 Debugging content issue...")

    try:
        # Authenticate
        auth = AuthHandler()
        client = await auth.authenticate()
        user_id = client.get_user_id()

        # Create a very simple post
        post = Post(
            title="Debug Content Test",
            subtitle="Testing why content doesn't appear",
            user_id=user_id,
        )

        # Add simple content
        print("📝 Adding content to post...")
        post.paragraph("This is paragraph 1.")
        post.heading("This is a heading", 2)
        post.paragraph("This is paragraph 2.")

        # Get draft data and inspect
        draft_data = post.get_draft()
        print("\n🔍 Draft data keys:", list(draft_data.keys()))
        print(f"Title: {draft_data.get('draft_title')}")
        print(f"Subtitle: {draft_data.get('draft_subtitle')}")

        # Check the body
        body_json_str = draft_data.get("draft_body", "{}")
        print(f"\n📄 Raw body JSON string: {body_json_str[:200]}...")

        # Parse and inspect body
        try:
            body_json = json.loads(body_json_str)
            print(f"\n📊 Body JSON structure:")
            print(json.dumps(body_json, indent=2))

            # Check content array
            content_array = body_json.get("content", [])
            print(f"\n📝 Number of content blocks: {len(content_array)}")

        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse body JSON: {e}")

        # Try to create the draft
        print("\n🚀 Creating draft...")
        result = client.post_draft(draft_data)
        draft_id = result.get("id")
        print(f"✅ Draft created: {draft_id}")

        # Get the draft back and check
        print("\n🔍 Fetching draft back...")
        fetched_draft = client.get_draft(draft_id)
        print(f"Fetched draft keys: {list(fetched_draft.keys())}")

        # Check if it has content
        if "body" in fetched_draft:
            print(f"Body present: {len(str(fetched_draft['body']))} chars")

    except Exception as e:
        print(f"❌ Debug failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(debug_content_issue())
