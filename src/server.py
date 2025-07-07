# ABOUTME: Main MCP server implementation for Substack MCP Plus
# ABOUTME: Provides tools for creating, updating, publishing posts with rich formatting

import asyncio
import logging
from typing import Any, Dict, List, Optional

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
from mcp.server.stdio import stdio_server

from src.handlers.auth_handler import AuthHandler
from src.handlers.post_handler import PostHandler
from src.handlers.image_handler import ImageHandler

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SubstackMCPServer:
    """MCP server for Substack operations"""
    
    def __init__(self):
        """Initialize the MCP server"""
        self.server = Server("substack-mcp-plus")
        self._initialize_handlers()
        self._register_handlers()
        
    def _initialize_handlers(self):
        """Initialize the Substack handlers"""
        try:
            self.auth_handler = AuthHandler()
            logger.info("Authentication handler initialized")
        except Exception as e:
            logger.error(f"Failed to initialize handlers: {e}")
            raise
            
    def _register_handlers(self):
        """Register all handlers with the MCP server"""
        
        @self.server.list_tools()
        async def handle_list_tools() -> List[Tool]:
            """List all available tools"""
            return [
                Tool(
                    name="create_formatted_post",
                    description="Create a new formatted draft post on Substack. Supports full markdown formatting. IMPORTANT: Always ask for user confirmation before creating new drafts. When user confirms with 'yes' or similar, call this tool again with confirm_create: true. The post will be saved as a draft.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "The main title/headline of the post. This will appear as the post title in Substack."
                            },
                            "content": {
                                "type": "string",
                                "description": "The full content of the post in markdown format. Supports all standard markdown: # headers, **bold**, *italic*, [links](url), lists, code blocks, > quotes. Use '<!-- PAYWALL -->' to add paywall marker."
                            },
                            "subtitle": {
                                "type": "string",
                                "description": "Optional subtitle that appears below the main title. Useful for additional context or taglines."
                            },
                            "confirm_create": {
                                "type": "boolean",
                                "description": "Must be set to true to confirm creating the draft. If not provided or false, a warning will be shown."
                            }
                        },
                        "required": ["title", "content"]
                    }
                ),
                Tool(
                    name="update_post",
                    description="Update an existing Substack draft post. Can modify title, content, subtitle, or any combination. IMPORTANT: Always ask for user confirmation before updating. When user confirms with 'yes' or similar, call this tool again with confirm_update: true. Use list_drafts first to get the post_id.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "post_id": {
                                "type": "string",
                                "description": "The unique ID of the draft post to update. Get this from list_drafts output."
                            },
                            "title": {
                                "type": "string",
                                "description": "New title for the post (optional). If provided, replaces the current title."
                            },
                            "content": {
                                "type": "string",
                                "description": "New content in markdown format (optional). If provided, replaces the entire current content."
                            },
                            "subtitle": {
                                "type": "string",
                                "description": "New subtitle for the post (optional). If provided, replaces the current subtitle."
                            },
                            "confirm_update": {
                                "type": "boolean",
                                "description": "Must be set to true to confirm the update. If not provided or false, a warning will be shown."
                            }
                        },
                        "required": ["post_id"]
                    }
                ),
                Tool(
                    name="publish_post",
                    description="Publish a draft post immediately to your Substack publication. This makes the post publicly visible to subscribers and sends it via email if enabled. IMPORTANT: Always ask for user confirmation before publishing. When user confirms with 'yes' or similar, call this tool again with confirm_publish: true. This action cannot be easily undone.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "post_id": {
                                "type": "string",
                                "description": "The unique ID of the draft post to publish. Get this from list_drafts output."
                            },
                            "confirm_publish": {
                                "type": "boolean",
                                "description": "Must be set to true to confirm publishing. If not provided or false, a warning will be shown."
                            }
                        },
                        "required": ["post_id"]
                    }
                ),
                Tool(
                    name="list_drafts",
                    description="List your recent draft posts with their titles and IDs. Use this to see what drafts are available for updating, publishing, or deleting. Returns basic info about each draft.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of drafts to return. Default is 10, maximum is 25.",
                                "default": 10
                            }
                        }
                    }
                ),
                Tool(
                    name="upload_image",
                    description="Upload an image file to Substack's CDN and get a URL that can be used in posts. Supports common image formats (JPG, PNG, GIF, WebP). The returned URL can be used in markdown content as ![alt text](url).",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "image_path": {
                                "type": "string",
                                "description": "Full file path to the image file to upload. Must be a valid image file on the local filesystem."
                            }
                        },
                        "required": ["image_path"]
                    }
                ),
                Tool(
                    name="delete_draft",
                    description="Safely delete a specific draft post with required confirmation. This permanently removes the draft from Substack and cannot be undone. Always shows a warning first if confirmation is missing.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "post_id": {
                                "type": "string",
                                "description": "The unique ID of the draft to delete. Get this from list_drafts output."
                            },
                            "confirm_delete": {
                                "type": "boolean",
                                "description": "Must be explicitly set to true to confirm deletion. This safety mechanism prevents accidental deletions."
                            }
                        },
                        "required": ["post_id", "confirm_delete"]
                    }
                ),
                Tool(
                    name="list_drafts_for_deletion",
                    description="Get detailed information about all drafts including titles, IDs, and last updated dates. Designed for reviewing drafts before deletion. Provides examples of how to safely delete each draft.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of drafts to return with full details. Default is 25, maximum is 25.",
                                "default": 25
                            }
                        }
                    }
                ),
                Tool(
                    name="list_published",
                    description="List your recently published posts with their titles, publication dates, and IDs. Use this to see what's already been published on your Substack.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of published posts to return. Default is 10, maximum is 25.",
                                "default": 10
                            }
                        }
                    }
                ),
                Tool(
                    name="get_post_content",
                    description="Read the full content of a specific post (draft or published) with all its formatting. Returns the post in a readable markdown format. Useful for reviewing content, copying from old posts, or checking formatting.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "post_id": {
                                "type": "string",
                                "description": "The ID of the post to read. Get this from list_drafts or list_published."
                            }
                        },
                        "required": ["post_id"]
                    }
                ),
                Tool(
                    name="duplicate_post",
                    description="Create a copy of an existing post as a new draft. Perfect for using posts as templates. IMPORTANT: Always ask for user confirmation before duplicating. When user confirms with 'yes' or similar, call this tool again with confirm_duplicate: true.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "post_id": {
                                "type": "string",
                                "description": "The ID of the post to duplicate."
                            },
                            "new_title": {
                                "type": "string",
                                "description": "Optional custom title for the duplicate. If not provided, will use 'Copy of [original title]'."
                            },
                            "confirm_duplicate": {
                                "type": "boolean",
                                "description": "Must be set to true to confirm duplication. If not provided or false, a warning will be shown."
                            }
                        },
                        "required": ["post_id"]
                    }
                ),
                Tool(
                    name="schedule_post",
                    description="Schedule a draft to be published at a specific date and time. The post will be automatically published at the scheduled time. IMPORTANT: Always ask for user confirmation before scheduling. When user confirms with 'yes' or similar, call this tool again with confirm_schedule: true. Time should be in ISO 8601 format (e.g., '2024-01-15T10:00:00Z').",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "post_id": {
                                "type": "string",
                                "description": "The ID of the draft to schedule."
                            },
                            "scheduled_at": {
                                "type": "string",
                                "description": "ISO 8601 datetime when to publish (e.g., '2024-01-15T10:00:00Z'). Must be in the future."
                            },
                            "confirm_schedule": {
                                "type": "boolean",
                                "description": "Must be set to true to confirm scheduling. If not provided or false, a warning will be shown."
                            }
                        },
                        "required": ["post_id", "scheduled_at"]
                    }
                ),
                Tool(
                    name="get_sections",
                    description="Get a list of available sections/categories in your Substack publication. Sections help organize your posts by topic or type. Returns section names and IDs that can be used when creating posts.",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                Tool(
                    name="get_subscriber_count",
                    description="Get the total number of subscribers to your Substack publication. Useful for tracking growth and understanding your audience size.",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                Tool(
                    name="preview_draft",
                    description="Generate a preview link for a draft post that can be shared with others for feedback. The preview link allows others to read the draft without it being published.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "post_id": {
                                "type": "string",
                                "description": "The ID of the draft to preview."
                            }
                        },
                        "required": ["post_id"]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Optional[Dict[str, Any]]) -> List[TextContent | ImageContent | EmbeddedResource]:
            """Handle tool execution"""
            try:
                # Authenticate and get client
                client = await self.auth_handler.authenticate()
                
                # Debug: Check if client is wrapped
                logger.debug(f"Client type after authenticate: {type(client)}")
                logger.debug(f"Client class: {client.__class__.__name__}")
                logger.debug(f"Is APIWrapper: {client.__class__.__name__ == 'APIWrapper'}")
                logger.debug(f"Client has get_draft: {hasattr(client, 'get_draft')}")
                
                if name == "create_formatted_post":
                    confirm = arguments.get("confirm_create", False)
                    
                    if not confirm:
                        # Show preview of what will be created
                        content_preview = arguments["content"][:200] + "..." if len(arguments["content"]) > 200 else arguments["content"]
                        
                        return [TextContent(
                            type="text",
                            text=f"⚠️ CONFIRMATION REQUIRED ⚠️\n\n"
                                 f"You are about to CREATE a new draft:\n"
                                 f"- Title: \"{arguments['title']}\"\n"
                                 f"- Subtitle: \"{arguments.get('subtitle', '[none]')}\"\n"
                                 f"- Content preview: {content_preview}\n\n"
                                 f"⚡ This will create a new draft in your Substack account.\n\n"
                                 f"Are you sure you want to create this draft?\n\n"
                                 f"To confirm, simply say \"yes\" or tell me to proceed.\n"
                                 f"To cancel, say \"no\" or tell me to stop."
                        )]
                    
                    # Proceed with creation
                    post_handler = PostHandler(client)
                    result = await post_handler.create_draft(
                        title=arguments["title"],
                        content=arguments["content"],
                        subtitle=arguments.get("subtitle"),
                        content_type="markdown"
                    )
                    return [TextContent(
                        type="text",
                        text=f"✅ Draft created successfully!\nID: {result.get('id')}\nTitle: {arguments['title']}"
                    )]
                    
                elif name == "update_post":
                    confirm = arguments.get("confirm_update", False)
                    
                    if not confirm:
                        # Get the draft details to show what will be updated
                        try:
                            draft = client.get_draft(arguments["post_id"])
                            
                            # Check if API returned a string error
                            if isinstance(draft, str):
                                raise ValueError(f"API error: {draft}")
                            if not isinstance(draft, dict):
                                raise ValueError("Invalid API response")
                                
                            current_title = draft.get('draft_title') or draft.get('title') or 'Untitled'
                            
                            changes = []
                            if arguments.get("title"):
                                changes.append(f"- Title: \"{arguments['title']}\"")
                            if arguments.get("subtitle") is not None:
                                changes.append(f"- Subtitle: \"{arguments['subtitle']}\"")
                            if arguments.get("content"):
                                changes.append("- Content: [new content provided]")
                            
                            changes_text = "\n".join(changes) if changes else "- No changes specified"
                            
                            return [TextContent(
                                type="text",
                                text=f"⚠️ CONFIRMATION REQUIRED ⚠️\n\n"
                                     f"You are about to UPDATE this draft:\n"
                                     f"- Post: \"{current_title}\"\n"
                                     f"- Changes:\n{changes_text}\n\n"
                                     f"⚡ This will ONLY update the fields listed above.\n"
                                     f"⚡ Other fields (like content) will remain unchanged.\n\n"
                                     f"Are you sure you want to update this draft?\n\n"
                                     f"To confirm, simply say \"yes\" or tell me to proceed.\n"
                                     f"To cancel, say \"no\" or tell me to stop."
                            )]
                        except Exception as e:
                            return [TextContent(
                                type="text",
                                text=f"⚠️ Error getting draft details: {str(e)}\n\n"
                                     f"Cannot proceed with update without confirmation."
                            )]
                    
                    # Proceed with update
                    post_handler = PostHandler(client)
                    result = await post_handler.update_draft(
                        post_id=arguments["post_id"],
                        title=arguments.get("title"),
                        content=arguments.get("content"),
                        subtitle=arguments.get("subtitle"),
                        content_type="markdown"
                    )
                    return [TextContent(
                        type="text",
                        text=f"✅ Post updated successfully!\nID: {arguments['post_id']}"
                    )]
                    
                elif name == "publish_post":
                    confirm = arguments.get("confirm_publish", False)
                    
                    if not confirm:
                        # Get the draft details to show what will be published
                        try:
                            draft = client.get_draft(arguments["post_id"])
                            
                            # Check if API returned a string error
                            if isinstance(draft, str):
                                raise ValueError(f"API error: {draft}")
                            if not isinstance(draft, dict):
                                raise ValueError("Invalid API response")
                                
                            title = draft.get('draft_title') or draft.get('title') or 'Untitled'
                            
                            # Check subscriber count if possible
                            try:
                                sections = client.get_sections()
                                pub_info = f"- Subscribers: {sections[0].get('subscriber_count', 'unknown')}"
                            except:
                                pub_info = "- Subscribers: [count unavailable]"
                            
                            return [TextContent(
                                type="text",
                                text=f"⚠️ CONFIRMATION REQUIRED ⚠️\n\n"
                                     f"You are about to PUBLISH this draft:\n"
                                     f"- Post: \"{title}\"\n"
                                     f"{pub_info}\n"
                                     f"- Action: Publish immediately and send to all subscribers\n\n"
                                     f"⚡ This CANNOT be undone and will send emails to all subscribers.\n\n"
                                     f"Are you sure you want to publish this post?\n\n"
                                     f"To confirm, simply say \"yes\" or tell me to proceed.\n"
                                     f"To cancel, say \"no\" or tell me to stop."
                            )]
                        except Exception as e:
                            return [TextContent(
                                type="text",
                                text=f"⚠️ Error getting draft details: {str(e)}\n\n"
                                     f"Cannot proceed with publishing without confirmation."
                            )]
                    
                    # Proceed with publishing
                    post_handler = PostHandler(client)
                    result = await post_handler.publish_draft(
                        post_id=arguments["post_id"]
                    )
                    return [TextContent(
                        type="text",
                        text=f"✅ Post published successfully!\nID: {arguments['post_id']}"
                    )]
                    
                elif name == "list_drafts":
                    post_handler = PostHandler(client)
                    drafts = await post_handler.list_drafts(
                        limit=arguments.get("limit", 10)
                    )
                    
                    draft_list = []
                    for draft in drafts:
                        title = draft.get('draft_title') or draft.get('title') or 'Untitled'
                        draft_id = draft.get('id')
                        draft_list.append(f"- {title} (ID: {draft_id})")
                    
                    return [TextContent(
                        type="text",
                        text=f"Found {len(drafts)} drafts:\n" + "\n".join(draft_list)
                    )]
                    
                elif name == "upload_image":
                    image_handler = ImageHandler(client)
                    result = await image_handler.upload_image(arguments["image_path"])
                    return [TextContent(
                        type="text",
                        text=f"Image uploaded successfully!\nURL: {result['url']}"
                    )]
                    
                elif name == "delete_draft":
                    post_id = arguments["post_id"]
                    confirm = arguments.get("confirm_delete", False)
                    
                    if not confirm:
                        return [TextContent(
                            type="text",
                            text=f"⚠️ DELETION REQUIRES CONFIRMATION ⚠️\n\n"
                                 f"You are about to delete draft ID: {post_id}\n"
                                 f"This action CANNOT be undone.\n\n"
                                 f"To proceed, call this tool again with:\n"
                                 f"- post_id: {post_id}\n"
                                 f"- confirm_delete: true"
                        )]
                    
                    # Get draft details before deletion
                    try:
                        draft = client.get_draft(post_id)
                        
                        # Check if API returned a string error
                        if isinstance(draft, str):
                            raise ValueError(f"API error: {draft}")
                        if not isinstance(draft, dict):
                            raise ValueError("Invalid API response")
                            
                        title = draft.get('draft_title') or draft.get('title') or 'Untitled'
                        
                        # Delete the draft
                        client.delete_draft(post_id)
                        
                        return [TextContent(
                            type="text",
                            text=f"✅ Draft deleted successfully!\n\n"
                                 f"Deleted: {title}\n"
                                 f"ID: {post_id}"
                        )]
                        
                    except Exception as e:
                        return [TextContent(
                            type="text",
                            text=f"❌ Failed to delete draft {post_id}: {str(e)}"
                        )]
                    
                elif name == "list_drafts_for_deletion":
                    post_handler = PostHandler(client)
                    drafts = await post_handler.list_drafts(
                        limit=arguments.get("limit", 50)
                    )
                    
                    if not drafts:
                        return [TextContent(
                            type="text",
                            text="No drafts found."
                        )]
                    
                    draft_details = []
                    draft_details.append(f"📝 Found {len(drafts)} drafts:")
                    draft_details.append("=" * 50)
                    
                    for i, draft in enumerate(drafts, 1):
                        title = draft.get('draft_title') or draft.get('title') or 'Untitled'
                        draft_id = draft.get('id')
                        updated = draft.get('draft_updated_at', 'Unknown')
                        
                        draft_details.append(f"{i}. {title}")
                        draft_details.append(f"   ID: {draft_id}")
                        draft_details.append(f"   Updated: {updated}")
                        draft_details.append("")
                    
                    draft_details.append("⚠️ To delete a specific draft:")
                    draft_details.append("Use delete_draft with post_id and confirm_delete: true")
                    draft_details.append("")
                    draft_details.append("💡 Example:")
                    draft_details.append(f"delete_draft(post_id=\"{drafts[0].get('id')}\", confirm_delete=true)")
                    
                    return [TextContent(
                        type="text",
                        text="\n".join(draft_details)
                    )]
                    
                elif name == "list_published":
                    post_handler = PostHandler(client)
                    published = await post_handler.list_published(
                        limit=arguments.get("limit", 10)
                    )
                    
                    if not published:
                        return [TextContent(
                            type="text",
                            text="No published posts found."
                        )]
                    
                    published_list = []
                    for post in published:
                        title = post.get('title', 'Untitled')
                        post_id = post.get('id')
                        post_date = post.get('post_date', 'Unknown date')
                        published_list.append(f"- {title} (ID: {post_id}, Published: {post_date})")
                    
                    return [TextContent(
                        type="text",
                        text=f"Found {len(published)} published posts:\n" + "\n".join(published_list)
                    )]
                    
                elif name == "get_post_content":
                    logger.debug(f"Creating PostHandler for get_post_content with client type: {type(client)}")
                    post_handler = PostHandler(client)
                    result = await post_handler.get_post_content(arguments["post_id"])
                    
                    content_text = []
                    content_text.append(f"📄 Post Content")
                    content_text.append("=" * 50)
                    content_text.append(f"Title: {result['title']}")
                    if result['subtitle']:
                        content_text.append(f"Subtitle: {result['subtitle']}")
                    content_text.append(f"Status: {result['status']}")
                    if result['publication_date']:
                        content_text.append(f"Published: {result['publication_date']}")
                    content_text.append(f"Audience: {result['audience']}")
                    content_text.append("")
                    content_text.append("Content:")
                    content_text.append("-" * 50)
                    content_text.append(result['content'])
                    
                    return [TextContent(
                        type="text",
                        text="\n".join(content_text)
                    )]
                    
                elif name == "duplicate_post":
                    logger.debug(f"Creating PostHandler for duplicate_post with client type: {type(client)}")
                    confirm = arguments.get("confirm_duplicate", False)
                    
                    if not confirm:
                        # Get the post details to show what will be duplicated
                        try:
                            post = client.get_draft(arguments["post_id"])
                            original_title = post.get('draft_title') or post.get('title') or 'Untitled'
                            new_title = arguments.get("new_title", f"Copy of {original_title}")
                            
                            return [TextContent(
                                type="text",
                                text=f"⚠️ CONFIRMATION REQUIRED ⚠️\n\n"
                                     f"You are about to DUPLICATE this post:\n"
                                     f"- Original: \"{original_title}\"\n"
                                     f"- New draft title: \"{new_title}\"\n\n"
                                     f"⚡ This will create a new draft with the same content.\n\n"
                                     f"Are you sure you want to duplicate this post?\n\n"
                                     f"To confirm, simply say \"yes\" or tell me to proceed.\n"
                                     f"To cancel, say \"no\" or tell me to stop."
                            )]
                        except Exception as e:
                            return [TextContent(
                                type="text",
                                text=f"⚠️ Error getting post details: {str(e)}\n\n"
                                     f"Cannot proceed with duplication without confirmation."
                            )]
                    
                    # Proceed with duplication
                    post_handler = PostHandler(client)
                    result = await post_handler.duplicate_post(
                        post_id=arguments["post_id"],
                        new_title=arguments.get("new_title")
                    )
                    
                    return [TextContent(
                        type="text",
                        text=f"✅ Post duplicated successfully!\n\n"
                             f"New draft ID: {result.get('id')}\n"
                             f"Title: {result.get('draft_title', 'Untitled')}"
                    )]
                    
                elif name == "schedule_post":
                    from datetime import datetime
                    confirm = arguments.get("confirm_schedule", False)
                    
                    if not confirm:
                        # Get the draft details to show what will be scheduled
                        try:
                            draft = client.get_draft(arguments["post_id"])
                            
                            # Check if API returned a string error
                            if isinstance(draft, str):
                                raise ValueError(f"API error: {draft}")
                            if not isinstance(draft, dict):
                                raise ValueError("Invalid API response")
                                
                            title = draft.get('draft_title') or draft.get('title') or 'Untitled'
                            
                            # Parse and format the datetime for display
                            scheduled_at = datetime.fromisoformat(arguments["scheduled_at"].replace('Z', '+00:00'))
                            formatted_time = scheduled_at.strftime("%B %d, %Y at %I:%M %p %Z")
                            
                            return [TextContent(
                                type="text",
                                text=f"⚠️ CONFIRMATION REQUIRED ⚠️\n\n"
                                     f"You are about to SCHEDULE this draft:\n"
                                     f"- Post: \"{title}\"\n"
                                     f"- Publish time: {formatted_time}\n\n"
                                     f"⚡ The post will automatically publish at this time.\n\n"
                                     f"Are you sure you want to schedule this post?\n\n"
                                     f"To confirm, simply say \"yes\" or tell me to proceed.\n"
                                     f"To cancel, say \"no\" or tell me to stop."
                            )]
                        except Exception as e:
                            return [TextContent(
                                type="text",
                                text=f"⚠️ Error getting draft details: {str(e)}\n\n"
                                     f"Cannot proceed with scheduling without confirmation."
                            )]
                    
                    # Proceed with scheduling
                    post_handler = PostHandler(client)
                    
                    # Parse the datetime string
                    scheduled_at = datetime.fromisoformat(arguments["scheduled_at"].replace('Z', '+00:00'))
                    
                    result = await post_handler.schedule_post(
                        post_id=arguments["post_id"],
                        scheduled_at=scheduled_at
                    )
                    
                    return [TextContent(
                        type="text",
                        text=f"📅 Post scheduled successfully!\n\n"
                             f"Post ID: {arguments['post_id']}\n"
                             f"Scheduled for: {arguments['scheduled_at']}"
                    )]
                    
                elif name == "get_sections":
                    post_handler = PostHandler(client)
                    sections = await post_handler.get_sections()
                    
                    if not sections:
                        return [TextContent(
                            type="text",
                            text="No sections found in your publication."
                        )]
                    
                    section_list = []
                    section_list.append("📁 Available Sections:")
                    section_list.append("=" * 50)
                    
                    for section in sections:
                        name = section.get('name', 'Unnamed')
                        section_id = section.get('id')
                        description = section.get('description', '')
                        
                        section_list.append(f"• {name} (ID: {section_id})")
                        if description:
                            section_list.append(f"  Description: {description}")
                    
                    return [TextContent(
                        type="text",
                        text="\n".join(section_list)
                    )]
                    
                elif name == "get_subscriber_count":
                    try:
                        post_handler = PostHandler(client)
                        result = await post_handler.get_subscriber_count()
                        
                        return [TextContent(
                            type="text",
                            text=f"📊 Subscriber Statistics\n"
                                 f"=" * 50 + "\n"
                                 f"Total Subscribers: {result['total_subscribers']:,}\n"
                                 f"Publication: {result['publication_url']}"
                        )]
                    except ValueError as e:
                        return [TextContent(
                            type="text",
                            text=f"❌ {str(e)}"
                        )]
                    except Exception as e:
                        logger.error(f"Unexpected error in get_subscriber_count: {str(e)}, type: {type(e)}")
                        return [TextContent(
                            type="text",
                            text=f"❌ Failed to get subscriber count: {str(e)}"
                        )]
                    
                elif name == "preview_draft":
                    try:
                        post_handler = PostHandler(client)
                        result = await post_handler.preview_draft(arguments["post_id"])
                        
                        preview_text = []
                        preview_text.append("🔗 Preview Generated")
                        preview_text.append("=" * 50)
                        preview_text.append(f"Post ID: {result['post_id']}")
                        
                        # Show the title if available
                        if result.get('title'):
                            preview_text.append(f"Title: {result['title']}")
                        
                        # Show the preview URL prominently
                        if result.get('preview_url'):
                            preview_text.append("")
                            preview_text.append(f"Preview URL: {result['preview_url']}")
                            preview_text.append("")
                            preview_text.append("Share this link for feedback before publishing!")
                        else:
                            preview_text.append("")
                            preview_text.append(result.get('message', 'Preview generated but URL not available'))
                        
                        return [TextContent(
                            type="text",
                            text="\n".join(preview_text)
                        )]
                    except ValueError as e:
                        return [TextContent(
                            type="text",
                            text=f"❌ {str(e)}"
                        )]
                    except Exception as e:
                        logger.error(f"Unexpected error in preview_draft: {str(e)}, type: {type(e)}")
                        return [TextContent(
                            type="text",
                            text=f"❌ Failed to generate preview: {str(e)}"
                        )]
                    
                else:
                    return [TextContent(
                        type="text",
                        text=f"Unknown tool: {name}"
                    )]
                    
            except Exception as e:
                logger.error(f"Error executing tool {name}: {e}")
                return [TextContent(
                    type="text",
                    text=f"Error: {str(e)}"
                )]
        
        logger.info(f"Registered 14 tools")
    
    async def run(self):
        """Run the MCP server using stdio transport"""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="substack-mcp-plus",
                    server_version="1.0.0",
                    capabilities={}
                )
            )


def main():
    """Main entry point"""
    try:
        server = SubstackMCPServer()
        asyncio.run(server.run())
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise


if __name__ == "__main__":
    main()