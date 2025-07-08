# ABOUTME: MCP tool for publishing Substack posts
# ABOUTME: Publishes draft posts immediately

from typing import Dict, Any


class PublishPostTool:
    """Tool for publishing posts on Substack"""

    def __init__(self, server):
        """Initialize the tool with server reference"""
        self.server = server
        self.name = "publish_post"
        self.description = "Publish a draft post immediately."
        self.input_schema = {
            "type": "object",
            "properties": {
                "post_id": {
                    "type": "string",
                    "description": "The ID of the draft post to publish",
                }
            },
            "required": ["post_id"],
        }

    async def execute(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the tool with given arguments"""
        post_id = arguments.get("post_id")

        if not post_id:
            raise ValueError("post_id is required")

        # Publish the post using PostHandler
        result = await self.server.post_handler.publish_draft(post_id=post_id)

        message = f"Successfully published post {post_id}"

        return {
            "success": True,
            "post_id": result.get("id"),
            "published": result.get("published", True),
            "url": result.get("url"),
            "message": message,
        }
