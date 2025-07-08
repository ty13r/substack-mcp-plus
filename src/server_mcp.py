#!/usr/bin/env python3
"""
Substack MCP Plus - Fixed MCP Server using proper SDK
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional

from mcp.server import Server, Request
from mcp.server.models import InitializationOptions
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource

from .handlers.auth_handler import AuthHandler
from .handlers.post_handler import PostHandler
from .handlers.image_handler import ImageHandler

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SubstackMCPServer:
    """MCP server for Substack operations"""

    def __init__(self):
        """Initialize the MCP server"""
        self.server = Server("substack-mcp-plus")
        self._initialize_handlers()
        self._register_tools()

    def _initialize_handlers(self):
        """Initialize the Substack handlers"""
        try:
            self.auth_handler = AuthHandler()
            logger.info("Authentication handler initialized")
        except Exception as e:
            logger.error(f"Failed to initialize handlers: {e}")
            raise

    def _register_tools(self):
        """Register all available tools with the MCP server"""

        @self.server.list_tools()
        async def handle_list_tools() -> List[Tool]:
            """List all available tools"""
            return [
                Tool(
                    name="create_formatted_post",
                    description="Create a formatted draft post on Substack with markdown content",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "The title of the post",
                            },
                            "content": {
                                "type": "string",
                                "description": "The content in markdown format",
                            },
                            "subtitle": {
                                "type": "string",
                                "description": "Optional subtitle for the post",
                            },
                        },
                        "required": ["title", "content"],
                    },
                ),
                Tool(
                    name="update_post",
                    description="Update an existing Substack draft",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "post_id": {
                                "type": "string",
                                "description": "The ID of the post to update",
                            },
                            "title": {
                                "type": "string",
                                "description": "New title (optional)",
                            },
                            "content": {
                                "type": "string",
                                "description": "New content in markdown format (optional)",
                            },
                            "subtitle": {
                                "type": "string",
                                "description": "New subtitle (optional)",
                            },
                        },
                        "required": ["post_id"],
                    },
                ),
                Tool(
                    name="publish_post",
                    description="Publish a draft post on Substack",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "post_id": {
                                "type": "string",
                                "description": "The ID of the draft to publish",
                            }
                        },
                        "required": ["post_id"],
                    },
                ),
                Tool(
                    name="list_drafts",
                    description="List recent draft posts",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "limit": {
                                "type": "integer",
                                "description": "Number of drafts to return (default: 10)",
                                "default": 10,
                            }
                        },
                    },
                ),
                Tool(
                    name="upload_image",
                    description="Upload an image to Substack's CDN",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "image_path": {
                                "type": "string",
                                "description": "Path to the image file to upload",
                            }
                        },
                        "required": ["image_path"],
                    },
                ),
            ]

        @self.server.call_tool()
        async def handle_call_tool(
            name: str, arguments: Optional[Dict[str, Any]]
        ) -> List[TextContent | ImageContent | EmbeddedResource]:
            """Handle tool execution"""
            try:
                # Authenticate and get client
                client = await self.auth_handler.authenticate()

                if name == "create_formatted_post":
                    post_handler = PostHandler(client)
                    result = await post_handler.create_draft(
                        title=arguments["title"],
                        content=arguments["content"],
                        subtitle=arguments.get("subtitle"),
                        content_type="markdown",
                    )
                    return [
                        TextContent(
                            type="text",
                            text=f"Draft created successfully!\nID: {result.get('id')}\nTitle: {arguments['title']}",
                        )
                    ]

                elif name == "update_post":
                    post_handler = PostHandler(client)
                    result = await post_handler.update_draft(
                        post_id=arguments["post_id"],
                        title=arguments.get("title"),
                        content=arguments.get("content"),
                        subtitle=arguments.get("subtitle"),
                        content_type="markdown",
                    )
                    return [
                        TextContent(
                            type="text",
                            text=f"Post updated successfully!\nID: {arguments['post_id']}",
                        )
                    ]

                elif name == "publish_post":
                    post_handler = PostHandler(client)
                    result = await post_handler.publish_draft(
                        post_id=arguments["post_id"]
                    )
                    return [
                        TextContent(
                            type="text",
                            text=f"Post published successfully!\nID: {arguments['post_id']}",
                        )
                    ]

                elif name == "list_drafts":
                    post_handler = PostHandler(client)
                    drafts = await post_handler.list_drafts(
                        limit=arguments.get("limit", 10)
                    )

                    draft_list = []
                    for draft in drafts:
                        title = (
                            draft.get("draft_title") or draft.get("title") or "Untitled"
                        )
                        draft_id = draft.get("id")
                        draft_list.append(f"- {title} (ID: {draft_id})")

                    return [
                        TextContent(
                            type="text",
                            text=f"Found {len(drafts)} drafts:\n"
                            + "\n".join(draft_list),
                        )
                    ]

                elif name == "upload_image":
                    image_handler = ImageHandler(
                        client, self.auth_handler.publication_name
                    )
                    result = await image_handler.upload_image(arguments["image_path"])
                    return [
                        TextContent(
                            type="text",
                            text=f"Image uploaded successfully!\nURL: {result['url']}",
                        )
                    ]

                else:
                    return [TextContent(type="text", text=f"Unknown tool: {name}")]

            except Exception as e:
                logger.error(f"Error executing tool {name}: {e}")
                return [TextContent(type="text", text=f"Error: {str(e)}")]

        logger.info(f"Registered {len(self.server.list_tools())} tools")

    async def run(self):
        """Run the MCP server using stdio transport"""
        from mcp.server.stdio import stdio_server

        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="substack-mcp-plus", server_version="1.0.0"
                ),
            )


def main():
    """Main entry point"""
    server = SubstackMCPServer()
    asyncio.run(server.run())


if __name__ == "__main__":
    main()
