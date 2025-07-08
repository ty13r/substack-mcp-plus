# ABOUTME: MCP tool for creating formatted Substack posts
# ABOUTME: Supports Markdown, HTML, and plain text with rich formatting

from typing import Dict, Any, Optional


class CreateFormattedPostTool:
    """Tool for creating formatted posts on Substack"""

    def __init__(self, server):
        """Initialize the tool with server reference"""
        self.server = server
        self.name = "create_formatted_post"
        self.description = "Create a new draft post on Substack with rich text formatting. Supports Markdown, HTML, and plain text."
        self.input_schema = {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "The title of the post"},
                "content": {
                    "type": "string",
                    "description": "The content of the post (Markdown, HTML, or plain text)",
                },
                "subtitle": {
                    "type": "string",
                    "description": "Optional subtitle for the post",
                },
                "content_type": {
                    "type": "string",
                    "enum": ["markdown", "html", "plain"],
                    "default": "markdown",
                    "description": "The format of the content",
                },
            },
            "required": ["title", "content"],
        }

    async def execute(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the tool with given arguments"""
        title = arguments.get("title")
        content = arguments.get("content")
        subtitle = arguments.get("subtitle")
        content_type = arguments.get("content_type", "markdown")

        if not title or not content:
            raise ValueError("Title and content are required")

        # Create the draft using PostHandler
        result = await self.server.post_handler.create_draft(
            title=title, content=content, subtitle=subtitle, content_type=content_type
        )

        return {
            "success": True,
            "post_id": result.get("id"),
            "title": result.get("title"),
            "subtitle": result.get("subtitle"),
            "url": result.get("url"),
            "message": f"Successfully created draft post: {title}",
        }
