#!/usr/bin/env python3
"""
Compare with a post that IS displaying content
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


async def compare_working_post():
    print("🔍 Comparing with working posts...")

    try:
        # Authenticate
        auth = AuthHandler()
        client = await auth.authenticate()

        # Get some published posts
        print("\n📋 Fetching published posts...")
        posts = list(client.get_published_posts())[:10]

        # Find a post that has content
        working_post = None
        for post in posts:
            if post.get("word_count", 0) > 100:  # Has substantial content
                working_post = post
                break

        if not working_post:
            print("❌ No working post found")
            return

        print(f"\n📄 Found working post: {working_post.get('title')}")
        print(f"   Word count: {working_post.get('word_count')}")
        print(f"   ID: {working_post.get('id')}")

        # Fetch the full post
        full_post = client.get_draft(working_post["id"])

        # Compare fields
        print("\n📊 Working post fields:")
        important_fields = ["type", "editor_v2", "body", "draft_body", "is_published"]
        for field in important_fields:
            value = full_post.get(field)
            if field in ["body", "draft_body"] and value:
                print(f"   {field}: {type(value).__name__} (length: {len(str(value))})")
                if isinstance(value, str) and value.startswith("{"):
                    try:
                        parsed = json.loads(value)
                        print(f"     - type: {parsed.get('type')}")
                        print(f"     - blocks: {len(parsed.get('content', []))}")
                    except:
                        pass
            else:
                print(f"   {field}: {value}")

        # Now fetch one of our empty posts
        print("\n\n📋 Comparing with our 'empty' post...")
        empty_post_id = "167625322"  # The one we just created

        empty_post = client.get_draft(empty_post_id)

        print("\n📊 'Empty' post fields:")
        for field in important_fields:
            value = empty_post.get(field)
            if field in ["body", "draft_body"] and value:
                print(f"   {field}: {type(value).__name__} (length: {len(str(value))})")
                if isinstance(value, str) and value.startswith("{"):
                    try:
                        parsed = json.loads(value)
                        print(f"     - type: {parsed.get('type')}")
                        print(f"     - blocks: {len(parsed.get('content', []))}")
                    except:
                        pass
            else:
                print(f"   {field}: {value}")

        # Check for differences
        print("\n\n⚠️  Key differences:")
        for field in full_post.keys():
            if field in empty_post:
                if full_post[field] != empty_post[field] and field not in [
                    "id",
                    "title",
                    "subtitle",
                    "body",
                    "draft_body",
                    "uuid",
                    "slug",
                ]:
                    print(f"   {field}: {full_post[field]} → {empty_post[field]}")

    except Exception as e:
        print(f"❌ Comparison failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(compare_working_post())
