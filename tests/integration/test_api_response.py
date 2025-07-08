#!/usr/bin/env python3
"""
Check what the API actually returns
"""

import pytest
import sys
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.handlers.auth_handler import AuthHandler


@pytest.mark.requires_auth
@pytest.mark.integration
async def test_api_response():
    print("🔍 Testing API responses...")

    try:
        # Authenticate
        auth = AuthHandler()
        client = await auth.authenticate()

        # Get the posts
        print("\n📋 Getting posts...")
        posts_gen = client.get_published_posts()

        # Get first few
        posts = []
        for i, post in enumerate(posts_gen):
            print(f"\nPost {i}: {type(post)}")
            if isinstance(post, dict):
                print(f"  Title: {post.get('title', 'No title')}")
                print(f"  ID: {post.get('id')}")
            else:
                print(f"  Value: {post}")

            posts.append(post)
            if i >= 2:  # Just get 3
                break

        # Try another approach - look at drafts
        print("\n\n📋 Getting drafts...")
        drafts_gen = client.get_drafts()

        for i, draft in enumerate(drafts_gen):
            print(f"\nDraft {i}: {type(draft)}")
            if isinstance(draft, dict):
                title = draft.get("draft_title", draft.get("title", "No title"))
                print(f"  Title: {title}")
                print(f"  ID: {draft.get('id')}")

                # Check if it has body
                has_body = "body" in draft
                has_draft_body = "draft_body" in draft
                print(f"  Has body: {has_body}")
                print(f"  Has draft_body: {has_draft_body}")

            if i >= 2:  # Just get 3
                break

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_api_response())
