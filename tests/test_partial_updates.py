"""Tests to verify partial updates work correctly"""
import pytest
from unittest.mock import Mock, AsyncMock
from src.handlers.post_handler import PostHandler


@pytest.fixture
def mock_client():
    """Create a mock Substack client"""
    client = Mock()
    client.put_draft = Mock(return_value={"id": "test-123"})
    client.get_user_id = Mock(return_value=12345)  # Return numeric ID
    return client


@pytest.fixture
def post_handler(mock_client):
    """Create a PostHandler instance with mock client"""
    return PostHandler(mock_client)


@pytest.mark.asyncio
class TestPartialUpdates:
    """Test that partial updates only send changed fields"""
    
    async def test_update_only_subtitle(self, post_handler, mock_client):
        """Test updating only the subtitle"""
        await post_handler.update_draft(
            post_id="test-123",
            subtitle="New subtitle only"
        )
        
        # Verify only subtitle was sent
        mock_client.put_draft.assert_called_once_with(
            "test-123",
            subtitle="New subtitle only"
        )
    
    async def test_update_only_title(self, post_handler, mock_client):
        """Test updating only the title"""
        await post_handler.update_draft(
            post_id="test-123",
            title="New title only"
        )
        
        # Verify only title was sent
        mock_client.put_draft.assert_called_once_with(
            "test-123",
            title="New title only"
        )
    
    async def test_update_only_content(self, post_handler, mock_client):
        """Test updating only the content"""
        await post_handler.update_draft(
            post_id="test-123",
            content="New content only",
            content_type="markdown"
        )
        
        # Verify only body was sent (content gets converted to body)
        args, kwargs = mock_client.put_draft.call_args
        assert args[0] == "test-123"
        assert "body" in kwargs
        assert "title" not in kwargs
        assert "subtitle" not in kwargs
    
    async def test_update_multiple_fields(self, post_handler, mock_client):
        """Test updating multiple fields at once"""
        await post_handler.update_draft(
            post_id="test-123",
            title="New title",
            subtitle="New subtitle"
        )
        
        # Verify both fields were sent
        mock_client.put_draft.assert_called_once_with(
            "test-123",
            title="New title",
            subtitle="New subtitle"
        )
    
    async def test_update_with_none_values_ignored(self, post_handler, mock_client):
        """Test that None values are not sent in updates"""
        await post_handler.update_draft(
            post_id="test-123",
            title="New title",
            subtitle=None,  # This should be ignored
            content=None    # This should be ignored
        )
        
        # Verify only title was sent
        mock_client.put_draft.assert_called_once_with(
            "test-123",
            title="New title"
        )
    
    async def test_update_empty_subtitle_allowed(self, post_handler, mock_client):
        """Test that empty string subtitle is allowed (to clear subtitle)"""
        await post_handler.update_draft(
            post_id="test-123",
            subtitle=""  # Empty string to clear subtitle
        )
        
        # Verify empty subtitle was sent
        mock_client.put_draft.assert_called_once_with(
            "test-123",
            subtitle=""
        )