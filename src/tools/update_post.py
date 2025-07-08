# ABOUTME: MCP tool for updating existing Substack posts
# ABOUTME: Allows updating title, subtitle, and content with formatting

from typing import Dict, Any, Optional


class UpdatePostTool:
    """Tool for updating existing posts on Substack"""

    def __init__(self, server):
        """Initialize the tool with server reference"""
        self.server = server
        self.name = "update_post"
        self.description = "Update an existing draft post on Substack. Can update title, subtitle, and/or content."
        self.input_schema = {
            "type": "object",
            "properties": {
                "post_id": {
                    "type": "string",
                    "description": "The ID of the post to update",
                },
                "title": {
                    "type": "string",
                    "description": "New title for the post (optional)",
                },
                "content": {
                    "type": "string",
                    "description": "New content for the post (optional)",
                },
                "subtitle": {
                    "type": "string",
                    "description": "New subtitle for the post (optional)",
                },
                "content_type": {
                    "type": "string",
                    "enum": ["markdown", "html", "plain"],
                    "default": "markdown",
                    "description": "The format of the content if content is provided",
                },
            },
            "required": ["post_id"],
        }

    async def execute(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the tool with given arguments"""
        post_id = arguments.get("post_id")
        title = arguments.get("title")
        content = arguments.get("content")
        subtitle = arguments.get("subtitle")
        content_type = arguments.get("content_type", "markdown")

        if not post_id:
            raise ValueError("post_id is required")

        # At least one field should be updated
        if not any([title, content, subtitle]):
            raise ValueError(
                "At least one of title, content, or subtitle must be provided"
            )

        # Update the post using PostHandler
        result = await self.server.post_handler.update_draft(
            post_id=post_id,
            title=title,
            content=content,
            subtitle=subtitle,
            content_type=content_type,
        )

        return {
            "success": True,
            "post_id": result.get("id"),
            "title": result.get("title"),
            "subtitle": result.get("subtitle"),
            "url": result.get("url"),
            "message": f"Successfully updated post: {post_id}",
        }
