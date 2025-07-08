#!/usr/bin/env python3
"""
Investigate the publish process
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


async def investigate_publish():
    print("🔍 Investigating publish process...")

    try:
        # Authenticate
        auth = AuthHandler()
        client = await auth.authenticate()
        user_id = client.get_user_id()

        # Create post with simple content
        post = Post(
            title="Publish Investigation",
            subtitle="Why is content missing?",
            user_id=user_id,
        )

        # Add content
        post.paragraph("First paragraph.")
        post.heading("My Heading", 2)
        post.paragraph("Second paragraph.")

        # Create draft
        draft_data = post.get_draft()
        result = client.post_draft(draft_data)
        draft_id = result.get("id")
        print(f"✅ Draft created: {draft_id}")

        # Check what prepublish_draft does
        print("\n🔍 Checking prepublish_draft...")
        try:
            prepub_result = client.prepublish_draft(draft_id)
            print(
                f"Prepublish result keys: {list(prepub_result.keys()) if prepub_result else 'None'}"
            )
        except Exception as e:
            print(f"Prepublish error: {e}")

        # Now publish
        print("\n🚀 Publishing...")
        pub_result = client.publish_draft(draft_id)

        # Check the published result
        print(f"\n📖 Published result:")
        print(f"  ID: {pub_result.get('id')}")
        print(f"  Title: {pub_result.get('title')}")
        print(f"  Type: {pub_result.get('type')}")

        # Check body vs draft_body
        body = pub_result.get("body")
        draft_body = pub_result.get("draft_body")

        print(f"\n📄 Content fields:")
        print(f"  body: {body}")
        print(f"  draft_body exists: {draft_body is not None}")

        if draft_body:
            parsed = json.loads(draft_body)
            print(f"  draft_body has content: {len(parsed.get('content', [])) > 0}")

        # Let's fetch the published post back
        print("\n🔍 Fetching published post back...")
        fetched = client.get_draft(draft_id)  # This should work for published posts too

        print(f"Fetched post type: {fetched.get('type')}")
        print(f"Fetched body: {fetched.get('body')}")
        print(f"Is published: {fetched.get('is_published')}")

    except Exception as e:
        print(f"❌ Investigation failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(investigate_publish())
