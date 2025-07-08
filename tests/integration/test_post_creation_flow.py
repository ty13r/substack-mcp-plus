import pytest

# ABOUTME: Integration tests for full post creation workflow
# ABOUTME: Tests the complete flow from markdown to published post

import pytest
import os
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime

from src.handlers.auth_handler import AuthHandler
from src.handlers.post_handler import PostHandler
from src.converters.markdown_converter import MarkdownConverter
from src.server import SubstackMCPServer


class TestPostCreationFlow:
    """Integration tests for post creation workflow"""

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_full_post_creation_flow(self):
        """Test creating a post from markdown through to draft creation"""
        # Set up environment
        with patch.dict(
            os.environ,
            {
                "SUBSTACK_EMAIL": "test@example.com",
                "SUBSTACK_PASSWORD": "testpass",
                "SUBSTACK_PUBLICATION_URL": "https://test.substack.com",
            },
        ):
            # Mock the Substack API client
            mock_client = Mock()
            mock_client.get_user_id = Mock(return_value=12345)  # Add numeric user ID
            mock_client.create_draft = Mock(
                return_value={
                    "id": "post-123",
                    "title": "My Test Post",
                    "subtitle": "A test subtitle",
                    "url": "https://test.substack.com/p/my-test-post",
                }
            )

            with patch(
                "src.handlers.auth_handler.SubstackApi", return_value=mock_client
            ):
                # Create auth and post handlers
                auth_handler = AuthHandler()
                client = await auth_handler.authenticate()
                post_handler = PostHandler(client)

                # Create a post with rich markdown content
                markdown_content = """# My Test Post

This is a test post with **bold** and *italic* text.

## Features

- Bullet point 1
- Bullet point 2
- Bullet point 3

### Code Example

```python
def hello_world():
    print("Hello, Substack!")
```

> This is a blockquote with some wisdom.

Check out [this link](https://example.com) for more info.

![Test Image](https://example.com/image.jpg "A test image")

---

That's all for now!"""

                # Need to use the mocked client directly
                mock_client.post_draft = Mock(
                    return_value={
                        "id": "post-123",
                        "title": "My Test Post",
                        "subtitle": "A test subtitle",
                        "url": "https://test.substack.com/p/my-test-post",
                    }
                )

                # Create the draft
                result = await post_handler.create_draft(
                    title="My Test Post",
                    content=markdown_content,
                    subtitle="A test subtitle",
                    content_type="markdown",
                )

                # Verify the result
                assert result["id"] == "post-123"
                assert result["title"] == "My Test Post"

                # Verify the API was called with properly formatted blocks
                mock_client.create_draft.assert_called_once()
                call_args = mock_client.create_draft.call_args[1]

                assert call_args["title"] == "My Test Post"
                assert call_args["subtitle"] == "A test subtitle"
                assert "body" in call_args

                blocks = call_args["body"]["blocks"]
                assert len(blocks) > 0

                # Verify specific block types were created
                block_types = [block["type"] for block in blocks]
                assert "heading-one" in block_types
                assert "heading-two" in block_types
                assert "heading-three" in block_types
                assert "paragraph" in block_types
                assert "bulleted-list" in block_types
                assert "code" in block_types
                assert "blockquote" in block_types
                assert "captioned-image" in block_types
                assert "hr" in block_types

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_mcp_server_create_post_flow(self):
        """Test creating a post through the MCP server"""
        with patch.dict(
            os.environ,
            {
                "SUBSTACK_EMAIL": "test@example.com",
                "SUBSTACK_PASSWORD": "testpass",
                "SUBSTACK_PUBLICATION_URL": "https://test.substack.com",
            },
        ):
            # Mock the Substack API
            mock_client = Mock()
            mock_client.create_draft = Mock(
                return_value={
                    "id": "post-456",
                    "title": "MCP Test Post",
                    "url": "https://test.substack.com/p/mcp-test-post",
                }
            )

            with patch(
                "src.handlers.auth_handler.SubstackApi", return_value=mock_client
            ):
                # Create MCP server
                server = SubstackMCPServer()

                # Call the create_formatted_post tool
                result = await server.handle_call_tool(
                    "create_formatted_post",
                    {
                        "title": "MCP Test Post",
                        "content": "# Hello from MCP\n\nThis is a test.",
                        "content_type": "markdown",
                    },
                )

                assert result["success"] is True
                assert result["post_id"] == "post-456"
                assert "Successfully created draft post" in result["message"]

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_update_and_publish_flow(self):
        """Test updating and publishing a post"""
        with patch.dict(
            os.environ,
            {
                "SUBSTACK_EMAIL": "test@example.com",
                "SUBSTACK_PASSWORD": "testpass",
                "SUBSTACK_PUBLICATION_URL": "https://test.substack.com",
            },
        ):
            # Mock the Substack API
            mock_client = Mock()
            mock_client.update_draft = Mock(
                return_value={"id": "post-789", "title": "Updated Post"}
            )
            mock_client.publish_draft = Mock(
                return_value={
                    "id": "post-789",
                    "published": True,
                    "url": "https://test.substack.com/p/updated-post",
                }
            )

            with patch(
                "src.handlers.auth_handler.SubstackApi", return_value=mock_client
            ):
                # Create handlers
                auth_handler = AuthHandler()
                client = await auth_handler.authenticate()
                post_handler = PostHandler(client)

                # Update the post
                update_result = await post_handler.update_draft(
                    post_id="post-789",
                    title="Updated Post",
                    content="# Updated Content\n\nThis has been updated.",
                )

                assert update_result["id"] == "post-789"
                mock_client.update_draft.assert_called_once()

                # Publish the post
                publish_result = await post_handler.publish_draft("post-789")

                assert publish_result["published"] is True
                mock_client.publish_draft.assert_called_once_with("post-789")

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_list_drafts_flow(self):
        """Test listing draft posts"""
        with patch.dict(
            os.environ,
            {
                "SUBSTACK_EMAIL": "test@example.com",
                "SUBSTACK_PASSWORD": "testpass",
                "SUBSTACK_PUBLICATION_URL": "https://test.substack.com",
            },
        ):
            # Mock the Substack API
            mock_client = Mock()
            mock_client.get_drafts = Mock(
                return_value=[
                    {"id": "1", "title": "Draft 1", "created_at": "2024-01-01"},
                    {"id": "2", "title": "Draft 2", "created_at": "2024-01-02"},
                    {"id": "3", "title": "Draft 3", "created_at": "2024-01-03"},
                ]
            )

            with patch(
                "src.handlers.auth_handler.SubstackApi", return_value=mock_client
            ):
                # Create MCP server
                server = SubstackMCPServer()

                # List drafts
                result = await server.handle_call_tool("list_drafts", {"limit": 10})

                assert result["success"] is True
                assert result["count"] == 3
                assert len(result["drafts"]) == 3
                assert result["drafts"][0]["title"] == "Draft 1"

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_error_handling(self):
        """Test error handling throughout the flow"""
        with patch.dict(
            os.environ,
            {
                "SUBSTACK_EMAIL": "test@example.com",
                "SUBSTACK_PASSWORD": "testpass",
                "SUBSTACK_PUBLICATION_URL": "https://test.substack.com",
            },
        ):
            # Mock API failure
            mock_client = Mock()
            mock_client.create_draft = Mock(side_effect=Exception("API Error"))

            with patch(
                "src.handlers.auth_handler.SubstackApi", return_value=mock_client
            ):
                auth_handler = AuthHandler()
                client = await auth_handler.authenticate()
                post_handler = PostHandler(client)

                # Attempt to create a post
                with pytest.raises(Exception, match="API Error"):
                    await post_handler.create_draft(title="Test", content="Content")
