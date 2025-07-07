# ABOUTME: MCP tool for publishing Substack posts
# ABOUTME: Supports immediate publishing or scheduling for future

from typing import Dict, Any, Optional
from datetime import datetime


class PublishPostTool:
    """Tool for publishing posts on Substack"""
    
    def __init__(self, server):
        """Initialize the tool with server reference"""
        self.server = server
        self.name = "publish_post"
        self.description = "Publish a draft post immediately or schedule it for a future date/time."
        self.input_schema = {
            "type": "object",
            "properties": {
                "post_id": {
                    "type": "string",
                    "description": "The ID of the draft post to publish"
                },
                "scheduled_at": {
                    "type": "string",
                    "description": "ISO 8601 datetime to schedule the post (optional). If not provided, publishes immediately."
                }
            },
            "required": ["post_id"]
        }
    
    async def execute(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the tool with given arguments"""
        post_id = arguments.get("post_id")
        scheduled_at_str = arguments.get("scheduled_at")
        
        if not post_id:
            raise ValueError("post_id is required")
        
        # Parse scheduled datetime if provided
        scheduled_at = None
        if scheduled_at_str:
            try:
                scheduled_at = datetime.fromisoformat(scheduled_at_str.replace('Z', '+00:00'))
            except ValueError:
                raise ValueError("scheduled_at must be a valid ISO 8601 datetime")
        
        # Publish the post using PostHandler
        result = await self.server.post_handler.publish_draft(
            post_id=post_id,
            scheduled_at=scheduled_at
        )
        
        if scheduled_at:
            message = f"Successfully scheduled post {post_id} for {scheduled_at_str}"
        else:
            message = f"Successfully published post {post_id}"
        
        return {
            "success": True,
            "post_id": result.get("id"),
            "published": result.get("published", False),
            "scheduled": result.get("scheduled", False),
            "scheduled_at": result.get("scheduled_at"),
            "url": result.get("url"),
            "message": message
        }