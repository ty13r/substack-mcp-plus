# ABOUTME: Debug tool to inspect the raw structure of a post
# ABOUTME: Returns detailed information about post fields and content structure

import json
from typing import Dict, Any


async def debug_post_structure(post_handler, post_id: str) -> Dict[str, Any]:
    """Debug tool to inspect post structure

    Args:
        post_handler: The PostHandler instance
        post_id: The ID of the post to inspect

    Returns:
        Detailed structure information
    """
    try:
        # Get the raw post data
        post = post_handler.client.get_draft(post_id)

        # Build debug info
        debug_info = {
            "post_id": post_id,
            "post_type": type(post).__name__,
            "post_keys": list(post.keys()) if isinstance(post, dict) else "Not a dict",
            "has_body": "body" in post if isinstance(post, dict) else False,
            "has_draft_body": "draft_body" in post if isinstance(post, dict) else False,
            "title_fields": {},
            "body_analysis": {},
            "sample_content": {},
        }

        if isinstance(post, dict):
            # Check title fields
            for field in ["title", "draft_title", "subtitle", "draft_subtitle"]:
                if field in post:
                    debug_info["title_fields"][field] = (
                        post[field][:50] + "..."
                        if len(str(post[field])) > 50
                        else post[field]
                    )

            # Analyze body structure
            for body_field in ["body", "draft_body"]:
                if body_field in post:
                    body = post[body_field]
                    debug_info["body_analysis"][body_field] = {
                        "type": type(body).__name__,
                        "is_dict": isinstance(body, dict),
                        "keys": (
                            list(body.keys())[:10] if isinstance(body, dict) else None
                        ),
                        "length": (
                            len(body) if isinstance(body, (str, list, dict)) else None
                        ),
                    }

                    # If it's a dict with blocks
                    if isinstance(body, dict) and "blocks" in body:
                        blocks = body["blocks"]
                        debug_info["body_analysis"][body_field]["blocks_info"] = {
                            "type": type(blocks).__name__,
                            "count": len(blocks) if isinstance(blocks, list) else 0,
                            "first_block": (
                                blocks[0]
                                if isinstance(blocks, list) and blocks
                                else None
                            ),
                        }

                    # Sample content
                    if isinstance(body, str):
                        debug_info["sample_content"][body_field] = (
                            body[:200] + "..." if len(body) > 200 else body
                        )
                    elif isinstance(body, dict):
                        debug_info["sample_content"][body_field] = (
                            json.dumps(body, indent=2)[:500] + "..."
                        )

        return debug_info

    except Exception as e:
        return {"error": str(e), "error_type": type(e).__name__}
