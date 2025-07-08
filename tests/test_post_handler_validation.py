# ABOUTME: Unit tests for PostHandler input validation - safe coverage boost
# ABOUTME: Tests validation logic without touching actual functionality

import pytest
from unittest.mock import Mock
from src.handlers.post_handler import PostHandler


class TestPostHandlerValidation:
    """Test input validation for PostHandler methods - no risk to functionality"""
    
    @pytest.fixture
    def mock_client(self):
        """Create a mock Substack client"""
        client = Mock()
        client.get_user_id.return_value = 123456
        client.publication_url = "https://test.substack.com"
        return client
    
    @pytest.fixture
    def post_handler(self, mock_client):
        """Create a PostHandler instance with mock client"""
        return PostHandler(mock_client)
    
    @pytest.mark.asyncio
    async def test_create_draft_title_validation(self, post_handler):
        """Test title validation in create_draft"""
        # Empty title
        with pytest.raises(ValueError, match="Title must be a non-empty string"):
            await post_handler.create_draft("", "content")
        
        # None title
        with pytest.raises(ValueError, match="Title must be a non-empty string"):
            await post_handler.create_draft(None, "content")
        
        # Title too long
        with pytest.raises(ValueError, match="Title must be 280 characters or less"):
            await post_handler.create_draft("x" * 281, "content")
    
    @pytest.mark.asyncio
    async def test_create_draft_content_validation(self, post_handler):
        """Test content validation in create_draft"""
        # Empty content
        with pytest.raises(ValueError, match="Content must be a non-empty string"):
            await post_handler.create_draft("Title", "")
        
        # None content
        with pytest.raises(ValueError, match="Content must be a non-empty string"):
            await post_handler.create_draft("Title", None)
    
    @pytest.mark.asyncio
    async def test_create_draft_subtitle_validation(self, post_handler):
        """Test subtitle validation in create_draft"""
        # Non-string subtitle
        with pytest.raises(ValueError, match="Subtitle must be a string if provided"):
            await post_handler.create_draft("Title", "content", subtitle=123)
        
        # Subtitle too long
        with pytest.raises(ValueError, match="Subtitle must be 280 characters or less"):
            await post_handler.create_draft("Title", "content", subtitle="x" * 281)
    
    @pytest.mark.asyncio
    async def test_create_draft_content_type_validation(self, post_handler):
        """Test content_type validation in create_draft"""
        # Invalid content type
        with pytest.raises(ValueError, match="content_type must be one of"):
            await post_handler.create_draft("Title", "content", content_type="invalid")
    
    @pytest.mark.asyncio
    async def test_update_draft_post_id_validation(self, post_handler):
        """Test post_id validation in update_draft"""
        # Empty post_id
        with pytest.raises(ValueError, match="post_id must be a non-empty string"):
            await post_handler.update_draft("")
        
        # None post_id
        with pytest.raises(ValueError, match="post_id must be a non-empty string"):
            await post_handler.update_draft(None)
    
    @pytest.mark.asyncio
    async def test_update_draft_title_validation(self, post_handler):
        """Test title validation in update_draft"""
        # Empty title when provided
        with pytest.raises(ValueError, match="Title must be a non-empty string if provided"):
            await post_handler.update_draft("post-123", title="")
        
        # Title too long
        with pytest.raises(ValueError, match="Title must be 280 characters or less"):
            await post_handler.update_draft("post-123", title="x" * 281)
    
    @pytest.mark.asyncio
    async def test_update_draft_subtitle_validation(self, post_handler):
        """Test subtitle validation in update_draft"""
        # Non-string subtitle
        with pytest.raises(ValueError, match="Subtitle must be a string if provided"):
            await post_handler.update_draft("post-123", subtitle=123)
        
        # Subtitle too long
        with pytest.raises(ValueError, match="Subtitle must be 280 characters or less"):
            await post_handler.update_draft("post-123", subtitle="x" * 281)
    
    @pytest.mark.asyncio
    async def test_update_draft_content_validation(self, post_handler):
        """Test content validation in update_draft"""
        # Empty content when provided
        with pytest.raises(ValueError, match="Content must be a non-empty string if provided"):
            await post_handler.update_draft("post-123", content="")
        
        # Invalid content type
        with pytest.raises(ValueError, match="content_type must be one of"):
            await post_handler.update_draft("post-123", content="test", content_type="invalid")
    
    @pytest.mark.asyncio
    async def test_publish_draft_validation(self, post_handler):
        """Test post_id validation in publish_draft"""
        # Empty post_id
        with pytest.raises(ValueError, match="post_id must be a non-empty string"):
            await post_handler.publish_draft("")
        
        # None post_id
        with pytest.raises(ValueError, match="post_id must be a non-empty string"):
            await post_handler.publish_draft(None)
    
    @pytest.mark.asyncio
    async def test_list_drafts_validation(self, post_handler):
        """Test limit validation in list_drafts"""
        # Non-integer limit
        with pytest.raises(ValueError, match="limit must be an integer"):
            await post_handler.list_drafts(limit="10")
        
        # Limit too small
        with pytest.raises(ValueError, match="limit must be between 1 and 25"):
            await post_handler.list_drafts(limit=0)
        
        # Limit too large
        with pytest.raises(ValueError, match="limit must be between 1 and 25"):
            await post_handler.list_drafts(limit=26)
    
    @pytest.mark.asyncio
    async def test_list_published_validation(self, post_handler):
        """Test limit validation in list_published"""
        # Non-integer limit
        with pytest.raises(ValueError, match="limit must be an integer"):
            await post_handler.list_published(limit="10")
        
        # Limit too small
        with pytest.raises(ValueError, match="limit must be between 1 and 25"):
            await post_handler.list_published(limit=0)
        
        # Limit too large  
        with pytest.raises(ValueError, match="limit must be between 1 and 25"):
            await post_handler.list_published(limit=26)