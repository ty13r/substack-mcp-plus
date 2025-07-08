# ABOUTME: MCP tool for listing draft Substack posts
# ABOUTME: Returns recent drafts with their metadata

from typing import Dict, Any, Optional


class ListDraftsTool:
    """Tool for listing draft posts on Substack"""

    def __init__(self, server):
        """Initialize the tool with server reference"""
        self.server = server
        self.name = "list_drafts"
        self.description = "List recent draft posts from your Substack publication."
        self.input_schema = {
            "type": "object",
            "properties": {
                "limit": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 50,
                    "default": 10,
                    "description": "Maximum number of drafts to return",
                }
            },
        }

    async def execute(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the tool with given arguments"""
        limit = arguments.get("limit", 10)

        # Validate limit
        if not isinstance(limit, int) or limit < 1 or limit > 50:
            raise ValueError("limit must be an integer between 1 and 50")

        # List drafts using PostHandler
        drafts = await self.server.post_handler.list_drafts(limit=limit)

        # Format the drafts for response
        formatted_drafts = []
        for draft in drafts:
            formatted_drafts.append(
                {
                    "id": draft.get("id"),
                    "title": draft.get("title"),
                    "subtitle": draft.get("subtitle"),
                    "created_at": draft.get("created_at"),
                    "updated_at": draft.get("updated_at"),
                    "word_count": draft.get("word_count"),
                    "url": draft.get("url"),
                }
            )

        return {
            "success": True,
            "drafts": formatted_drafts,
            "count": len(formatted_drafts),
            "message": f"Found {len(formatted_drafts)} draft(s)",
        }
