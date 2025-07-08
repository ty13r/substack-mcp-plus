# ABOUTME: Unit tests for upload_image MCP tool
# ABOUTME: Tests image upload functionality through the MCP interface

import pytest
from unittest.mock import Mock, AsyncMock, patch
from src.tools.upload_image_tool import UploadImageTool


class TestUploadImageTool:
    """Test suite for upload_image MCP tool"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.mock_server = Mock()
        self.mock_client = Mock()
        self.mock_post_handler = Mock()
        self.mock_post_handler.client = self.mock_client
        self.mock_server.post_handler = self.mock_post_handler
        self.tool = UploadImageTool(self.mock_server)
    
    @pytest.mark.asyncio
    async def test_tool_metadata(self):
        """Test tool has correct metadata"""
        assert self.tool.name == "upload_image"
        assert "Upload an image" in self.tool.description
        assert self.tool.input_schema["required"] == ["source"]
        assert "source" in self.tool.input_schema["properties"]
        assert "optimize_for" in self.tool.input_schema["properties"]
        assert "caption" in self.tool.input_schema["properties"]
    
    @pytest.mark.asyncio
    async def test_upload_image_web_optimization(self):
        """Test uploading image with web optimization"""
        with patch('src.tools.upload_image_tool.ImageHandler') as mock_handler_class:
            # Mock ImageHandler instance
            mock_handler = Mock()
            mock_handler.upload_image = AsyncMock(return_value={
                "url": "https://substackcdn.com/image/original.jpg",
                "id": "image-123",
                "filename": "test.jpg"
            })
            mock_handler.get_optimized_url = Mock(
                return_value="https://substackcdn.com/image/fetch/w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https://example.com/test.jpg"
            )
            mock_handler_class.return_value = mock_handler
            
            result = await self.tool.execute({
                "source": "/path/to/image.jpg",
                "optimize_for": "web"
            })
            
            assert result["success"] is True
            assert "w_1456" in result["url"]
            assert result["optimization"] == "web"
            assert result["id"] == "image-123"
            assert "successfully" in result["message"]
    
    @pytest.mark.asyncio
    async def test_upload_image_email_optimization(self):
        """Test uploading with email optimization"""
        with patch('src.tools.upload_image_tool.ImageHandler') as mock_handler_class:
            mock_handler = Mock()
            mock_handler.upload_image = AsyncMock(return_value={
                "url": "https://substackcdn.com/image/original.jpg",
                "id": "image-456",
                "filename": "email.jpg"
            })
            mock_handler.get_optimized_url = Mock(
                return_value="https://substackcdn.com/image/fetch/w_600,c_limit,f_auto,q_auto:good,fl_progressive:steep/https://example.com/email.jpg"
            )
            mock_handler_class.return_value = mock_handler
            
            result = await self.tool.execute({
                "source": "https://example.com/remote.jpg",
                "optimize_for": "email",
                "caption": "Email header image"
            })
            
            assert result["success"] is True
            assert "w_600" in result["url"]
            assert result["optimization"] == "email"
            assert result["caption"] == "Email header image"
    
    @pytest.mark.asyncio
    async def test_upload_image_thumbnail_optimization(self):
        """Test uploading with thumbnail optimization"""
        with patch('src.tools.upload_image_tool.ImageHandler') as mock_handler_class:
            mock_handler = Mock()
            mock_handler.upload_image = AsyncMock(return_value={
                "url": "https://substackcdn.com/image/original.jpg",
                "id": "image-789"
            })
            mock_handler.get_optimized_url = Mock(
                return_value="https://substackcdn.com/image/fetch/w_300,c_limit,f_auto,q_auto:low,fl_progressive:steep/https://example.com/thumb.jpg"
            )
            mock_handler_class.return_value = mock_handler
            
            result = await self.tool.execute({
                "source": "/path/to/large.jpg",
                "optimize_for": "thumbnail"
            })
            
            assert result["success"] is True
            assert "w_300" in result["url"]
            assert "q_auto:low" in result["url"]
            assert result["optimization"] == "thumbnail"
    
    @pytest.mark.asyncio
    async def test_upload_image_default_optimization(self):
        """Test uploading with default (web) optimization"""
        with patch('src.tools.upload_image_tool.ImageHandler') as mock_handler_class:
            mock_handler = Mock()
            mock_handler.upload_image = AsyncMock(return_value={
                "url": "https://substackcdn.com/image/original.jpg",
                "id": "image-default"
            })
            mock_handler.get_optimized_url = Mock(
                return_value="https://substackcdn.com/image/fetch/w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https://example.com/default.jpg"
            )
            mock_handler_class.return_value = mock_handler
            
            result = await self.tool.execute({
                "source": "/path/to/image.jpg"
                # No optimize_for specified, should default to "web"
            })
            
            assert result["success"] is True
            assert "w_1456" in result["url"]
            assert result["optimization"] == "web"
    
    @pytest.mark.asyncio
    async def test_upload_image_missing_source(self):
        """Test error when source is missing"""
        with pytest.raises(ValueError, match="source is required"):
            await self.tool.execute({})
    
    @pytest.mark.asyncio
    async def test_upload_image_file_not_found(self):
        """Test handling file not found error"""
        with patch('src.tools.upload_image_tool.ImageHandler') as mock_handler_class:
            mock_handler = Mock()
            mock_handler.upload_image = AsyncMock(
                side_effect=FileNotFoundError("Image file not found")
            )
            mock_handler_class.return_value = mock_handler
            
            result = await self.tool.execute({
                "source": "/nonexistent/image.jpg"
            })
            
            assert result["success"] is False
            assert "File not found" in result["error"]
    
    @pytest.mark.asyncio
    async def test_upload_image_invalid_format(self):
        """Test handling invalid image format"""
        with patch('src.tools.upload_image_tool.ImageHandler') as mock_handler_class:
            mock_handler = Mock()
            mock_handler.upload_image = AsyncMock(
                side_effect=ValueError("Unsupported image format")
            )
            mock_handler_class.return_value = mock_handler
            
            result = await self.tool.execute({
                "source": "/path/to/document.pdf"
            })
            
            assert result["success"] is False
            assert "Invalid image" in result["error"]
    
    @pytest.mark.asyncio
    async def test_upload_image_generic_error(self):
        """Test handling generic upload errors"""
        with patch('src.tools.upload_image_tool.ImageHandler') as mock_handler_class:
            mock_handler = Mock()
            mock_handler.upload_image = AsyncMock(
                side_effect=Exception("Network error")
            )
            mock_handler_class.return_value = mock_handler
            
            result = await self.tool.execute({
                "source": "https://example.com/image.jpg"
            })
            
            assert result["success"] is False
            assert "Upload failed" in result["error"]
            assert "Network error" in result["error"]
    
    @pytest.mark.asyncio
    async def test_preserves_original_url(self):
        """Test that both original and optimized URLs are returned"""
        original_url = "https://substackcdn.com/image/original.jpg"
        optimized_url = "https://substackcdn.com/image/optimized.jpg"
        
        with patch('src.tools.upload_image_tool.ImageHandler') as mock_handler_class:
            mock_handler = Mock()
            mock_handler.upload_image = AsyncMock(return_value={
                "url": original_url,
                "id": "image-999",
                "filename": "test.jpg"
            })
            mock_handler.get_optimized_url = Mock(return_value=optimized_url)
            mock_handler_class.return_value = mock_handler
            
            result = await self.tool.execute({
                "source": "/path/to/image.jpg"
            })
            
            assert result["success"] is True
            assert result["original_url"] == original_url
            assert result["url"] == optimized_url
            assert result["url"] != result["original_url"]