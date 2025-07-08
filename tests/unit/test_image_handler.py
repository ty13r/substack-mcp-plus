# ABOUTME: Unit tests for ImageHandler class that manages image uploads to Substack CDN
# ABOUTME: Tests uploading images and getting CDN URLs

import pytest
from unittest.mock import Mock, patch, MagicMock, AsyncMock, MagicMock
import io
import aiohttp
from src.handlers.image_handler import ImageHandler


class TestImageHandler:
    """Test suite for ImageHandler class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.mock_client = Mock()
        self.handler = ImageHandler(self.mock_client)
    
    @pytest.mark.asyncio
    async def test_upload_image_from_file_path(self):
        """Test uploading an image from a file path"""
        # Mock file reading
        mock_image_data = b"fake image data"
        
        with patch("os.path.exists", return_value=True):
            with patch("builtins.open", MagicMock(return_value=io.BytesIO(mock_image_data))):
                # Mock the get_image response
                self.mock_client.get_image = Mock(return_value={
                    "url": "https://substackcdn.com/image/fetch/w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https://example.com/uploaded.jpg",
                    "id": "image-123",
                    "contentType": "image/jpeg",
                    "bytes": 12345,
                    "imageWidth": 800,
                    "imageHeight": 600
                })
                
                result = await self.handler.upload_image("/path/to/image.jpg")
                
                assert result["url"] == "https://substackcdn.com/image/fetch/w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https://example.com/uploaded.jpg"
                assert result["id"] == "image-123"
                self.mock_client.get_image.assert_called_once_with("/path/to/image.jpg")
    
    @pytest.mark.asyncio
    async def test_upload_image_from_url(self):
        """Test uploading an image from a URL"""
        image_url = "https://example.com/remote-image.jpg"
        
        # Mock the get_image response for URL
        self.mock_client.get_image = Mock(return_value={
            "url": "https://substackcdn.com/image/fetch/w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https://example.com/uploaded.jpg",
            "id": "image-456",
            "contentType": "image/jpeg",
            "bytes": 12345,
            "imageWidth": 800,
            "imageHeight": 600
        })
        
        result = await self.handler.upload_image(image_url)
        
        assert result["url"] == "https://substackcdn.com/image/fetch/w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https://example.com/uploaded.jpg"
        assert result["id"] == "image-456"
        self.mock_client.get_image.assert_called_once_with(image_url)
    
    @pytest.mark.asyncio
    async def test_upload_image_with_bytes(self):
        """Test uploading image data directly"""
        image_data = b"direct image bytes"
        
        self.mock_client.get_image = Mock(return_value={
            "url": "https://substackcdn.com/image/fetch/w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https://example.com/uploaded.jpg",
            "id": "image-789",
            "contentType": "image/jpeg",
            "bytes": 12345,
            "imageWidth": 800,
            "imageHeight": 600
        })
        
        with patch("tempfile.mkstemp", return_value=(999, "/tmp/tmpfile.jpg")):
            with patch("os.chmod"):
                with patch("os.fdopen", return_value=io.BytesIO()):
                    with patch("os.unlink"):
                        result = await self.handler.upload_image(image_data, filename="custom.jpg")
        
        assert result["url"] == "https://substackcdn.com/image/fetch/w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https://example.com/uploaded.jpg"
        assert result["id"] == "image-789"
        assert result["filename"] == "custom.jpg"
    
    @pytest.mark.asyncio
    async def test_validate_image_format(self):
        """Test image format validation"""
        # Valid formats
        assert self.handler._validate_image_format("image.jpg") is True
        assert self.handler._validate_image_format("photo.jpeg") is True
        assert self.handler._validate_image_format("pic.png") is True
        assert self.handler._validate_image_format("graphic.gif") is True
        assert self.handler._validate_image_format("IMAGE.JPG") is True  # Case insensitive
        
        # Invalid formats
        assert self.handler._validate_image_format("document.pdf") is False
        assert self.handler._validate_image_format("video.mp4") is False
        assert self.handler._validate_image_format("file.txt") is False
        assert self.handler._validate_image_format("noextension") is False
    
    @pytest.mark.asyncio
    async def test_upload_invalid_format(self):
        """Test uploading an invalid image format"""
        with patch("os.path.exists", return_value=True):
            with pytest.raises(ValueError, match="Unsupported image format"):
                await self.handler.upload_image("/path/to/document.pdf")
    
    @pytest.mark.asyncio
    async def test_upload_file_not_found(self):
        """Test handling file not found error"""
        with patch("os.path.exists", return_value=False):
            with pytest.raises(FileNotFoundError, match="Image file not found"):
                await self.handler.upload_image("/nonexistent/image.jpg")
    
    @pytest.mark.asyncio
    async def test_upload_url_fetch_error(self):
        """Test handling URL fetch errors"""
        image_url = "https://example.com/bad-image.jpg"
        
        # Mock the get_image method to raise an exception
        self.mock_client.get_image = Mock(side_effect=Exception("Failed to fetch image"))
        
        with pytest.raises(Exception, match="Failed to fetch image"):
            await self.handler.upload_image(image_url)
    
    @pytest.mark.asyncio
    async def test_upload_api_error(self):
        """Test handling Substack API errors"""
        self.mock_client.get_image = Mock(side_effect=Exception("API Error"))
        
        with patch("os.path.exists", return_value=True):
            with pytest.raises(Exception, match="API Error"):
                await self.handler.upload_image("/path/to/image.jpg")
    
    def test_get_optimized_url(self):
        """Test getting optimized image URLs"""
        original_url = "https://substackcdn.com/image/fetch/f_auto,q_auto:good,fl_progressive:steep/https://example.com/image.jpg"
        
        # Test different size options
        small_url = self.handler.get_optimized_url(original_url, width=300)
        assert "w_300" in small_url
        
        medium_url = self.handler.get_optimized_url(original_url, width=800)
        assert "w_800" in medium_url
        
        # Test with quality setting
        low_quality_url = self.handler.get_optimized_url(original_url, quality="auto:low")
        assert "q_auto:low" in low_quality_url
        
        # Test with format
        webp_url = self.handler.get_optimized_url(original_url, format="webp")
        assert "f_webp" in webp_url
    
    @pytest.mark.asyncio
    async def test_batch_upload(self):
        """Test uploading multiple images"""
        image_paths = ["/path/to/image1.jpg", "/path/to/image2.png", "/path/to/image3.gif"]
        
        with patch("os.path.exists", return_value=True):
            # Need to create a new mock for each file open
            mock_files = [io.BytesIO(b"image data") for _ in range(3)]
            mock_open = MagicMock(side_effect=mock_files)
            
            with patch("builtins.open", mock_open):
                self.mock_client.get_image = Mock(side_effect=[
                    {"url": f"https://substackcdn.com/image{i}.jpg", "id": f"image-{i}", "contentType": "image/jpeg", "bytes": 12345, "imageWidth": 800, "imageHeight": 600}
                    for i in range(1, 4)
                ])
                
                results = await self.handler.batch_upload(image_paths)
                
                assert len(results) == 3
                assert all(r["success"] for r in results)
                assert results[0]["url"] == "https://substackcdn.com/image1.jpg"
                assert results[2]["id"] == "image-3"