#!/usr/bin/env python3
"""
Test how the Post object structures content
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
async def test_post_structure():
    print("🔍 Testing Post object structure...")

    # Authenticate
    auth = AuthHandler()
    client = await auth.authenticate()
    user_id = client.get_user_id()

    # Create a simple post
    post = Post(
        title="Debug Post Structure",
        subtitle="Testing content structure",
        user_id=user_id,
    )

    # Test 1: Simple paragraph
    print("\n📝 Test 1: Adding simple paragraph...")
    post.paragraph("This is a simple paragraph.")

    # Test 2: Paragraph with formatting
    print("📝 Test 2: Adding formatted paragraph...")
    post.paragraph().text("This is ").text("bold").marks([{"type": "strong"}]).text(
        " text."
    )

    # Test 3: Try code block via add
    print("📝 Test 3: Trying code block via add()...")
    post.add({"type": "code_block", "content": 'def test():\n    return "test"'})

    # Get the draft structure
    draft_data = post.get_draft()

    print("\n🔍 Draft structure:")
    print(f"Title: {draft_data.get('draft_title')}")
    print(f"Subtitle: {draft_data.get('draft_subtitle')}")

    # Parse the body JSON
    body_json = json.loads(draft_data.get("draft_body", "{}"))
    print(f"\n📄 Body structure:")
    print(json.dumps(body_json, indent=2))

    print("\n🔍 Content blocks:")
    for i, block in enumerate(body_json.get("content", [])):
        print(f"\nBlock {i + 1}:")
        print(f"  Type: {block.get('type')}")
        if "content" in block:
            print(f"  Content: {block.get('content')}")
        if "attrs" in block:
            print(f"  Attrs: {block.get('attrs')}")


if __name__ == "__main__":
    asyncio.run(test_post_structure())
