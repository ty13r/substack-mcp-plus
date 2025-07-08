"""Safe coverage improvement tests targeting public APIs only."""

import os
import unittest
from unittest.mock import Mock, patch, MagicMock, AsyncMock
import json
import tempfile
from datetime import datetime

# Import the modules we're testing
from src.handlers.auth_handler import AuthHandler
from src.handlers.post_handler import PostHandler
from src.handlers.image_handler import ImageHandler
from src.converters.html_converter import HTMLConverter
from src.converters.markdown_converter import MarkdownConverter


class TestSafeCoverage(unittest.TestCase):
    """Tests designed to improve coverage without breaking functionality."""

    def test_auth_handler_publication_extraction(self):
        """Test publication name extraction from various URL formats."""
        # Mock environment variables
        with patch.dict(
            os.environ,
            {
                "SUBSTACK_EMAIL": "test@example.com",
                "SUBSTACK_PASSWORD": "testpass",
                "SUBSTACK_PUBLICATION_URL": "https://example.substack.com",
            },
        ):
            auth = AuthHandler()
            result = auth._extract_publication_name("https://example.substack.com")
            self.assertEqual(result, "example")

        # Test URL with path
        with patch.dict(
            os.environ,
            {
                "SUBSTACK_EMAIL": "test@example.com",
                "SUBSTACK_PASSWORD": "testpass",
                "SUBSTACK_PUBLICATION_URL": "https://example.substack.com/archive",
            },
        ):
            auth = AuthHandler()
            result = auth._extract_publication_name(
                "https://example.substack.com/archive"
            )
            self.assertEqual(result, "example")

    def test_post_handler_content_conversion(self):
        """Test post handler content conversion methods."""
        mock_client = Mock()
        handler = PostHandler(mock_client)

        # Test plain text to blocks conversion
        text = "Hello World"
        blocks = handler._plain_text_to_blocks(text)
        self.assertEqual(len(blocks), 1)
        self.assertEqual(blocks[0]["type"], "paragraph")

        # Test content to blocks conversion
        blocks = handler._convert_content_to_blocks("# Title", "markdown")
        self.assertTrue(len(blocks) > 0)

    def test_html_converter_image_handling(self):
        """Test HTML converter's image processing."""
        converter = HTMLConverter()

        # Test image with caption - check the actual structure
        html = '<figure><img src="test.jpg" alt="Test"><figcaption>Caption</figcaption></figure>'
        result = converter.convert(html)
        # The converter might create a paragraph with image and caption text
        self.assertTrue(len(result) > 0)

        # Test standalone image
        html = '<img src="test.jpg" alt="Test">'
        result = converter.convert(html)
        self.assertTrue(len(result) > 0)

    def test_markdown_converter_formatting(self):
        """Test markdown converter's formatting options."""
        converter = MarkdownConverter()

        # Test bold text
        md = "**Bold text**"
        result = converter.convert(md)
        # Check for strong mark
        self.assertTrue(any("strong" in str(block) for block in result))

        # Test italic text
        md = "*Italic text*"
        result = converter.convert(md)
        # Check for em mark
        self.assertTrue(any("em" in str(block) for block in result))

    def test_converters_edge_cases(self):
        """Test converters with edge cases."""
        # Test HTML converter with empty content
        html_converter = HTMLConverter()
        result = html_converter.convert("")
        self.assertEqual(result, [])

        # Test Markdown converter with empty content
        md_converter = MarkdownConverter()
        result = md_converter.convert("")
        # Empty markdown might return empty list
        self.assertIsInstance(result, list)

    def test_handlers_initialization(self):
        """Test handler initialization."""
        # Test auth handler initialization with all required env vars
        with patch.dict(
            os.environ,
            {
                "SUBSTACK_EMAIL": "test@example.com",
                "SUBSTACK_PASSWORD": "testpass",
                "SUBSTACK_PUBLICATION_URL": "https://example.substack.com",
            },
        ):
            auth = AuthHandler()
            self.assertIsNotNone(auth)
            self.assertEqual(auth.email, "test@example.com")

        # Test post handler initialization with mock client
        post = PostHandler(Mock())
        self.assertIsNotNone(post.client)

        # Test image handler initialization with mock client
        image = ImageHandler(Mock())
        self.assertIsNotNone(image.client)

    def test_converter_block_structures(self):
        """Test converter block structures."""
        # Test HTML converter creates proper blocks
        html_converter = HTMLConverter()
        html = "<h1>Title</h1><p>Paragraph</p>"
        result = html_converter.convert(html)
        # Should have heading and paragraph blocks
        types = [block.get("type") for block in result]
        # The heading might be 'heading-one' not 'heading'
        self.assertTrue(any("heading" in t for t in types if t))
        self.assertIn("paragraph", types)

        # Test Markdown converter creates proper blocks
        md_converter = MarkdownConverter()
        md = "# Title\n\nParagraph"
        result = md_converter.convert(md)
        types = [block.get("type") for block in result]
        self.assertTrue(any("heading" in t for t in types if t))
        self.assertIn("paragraph", types)

    def test_html_converter_list_processing(self):
        """Test HTML converter's list handling."""
        converter = HTMLConverter()

        # Test unordered list
        html = "<ul><li>Item 1</li><li>Item 2</li></ul>"
        result = converter.convert(html)
        # Check for bulleted list block
        self.assertTrue(any(block.get("type") == "bulleted-list" for block in result))

        # Test ordered list
        html = "<ol><li>First</li><li>Second</li></ol>"
        result = converter.convert(html)
        # Check for ordered list block
        self.assertTrue(any(block.get("type") == "ordered-list" for block in result))

    def test_markdown_converter_code_blocks(self):
        """Test markdown converter's code block handling."""
        converter = MarkdownConverter()

        # Test code block
        md = '```python\nprint("Hello")\n```'
        result = converter.convert(md)
        # Check for code block
        self.assertTrue(any(block.get("type") == "code" for block in result))

        # Test inline code
        md = "Use `print()` function"
        result = converter.convert(md)
        # Check for code mark
        self.assertTrue(any("code" in str(block) for block in result))

    def test_image_handler_validation(self):
        """Test image handler validation methods."""
        mock_client = Mock()
        handler = ImageHandler(mock_client)

        # Test image format validation
        self.assertTrue(handler._validate_image_format("test.jpg"))
        self.assertTrue(handler._validate_image_format("test.png"))
        self.assertTrue(handler._validate_image_format("test.gif"))
        self.assertFalse(handler._validate_image_format("test.txt"))

        # Test optimized URL generation with non-Substack URL (should return as-is)
        result = handler.get_optimized_url("https://example.com/image.jpg", width=800)
        self.assertEqual(result, "https://example.com/image.jpg")

        # Test with Substack CDN URL
        substack_url = "https://substackcdn.com/image/fetch/f_auto,q_auto:good/https://example.com/image.jpg"
        result = handler.get_optimized_url(substack_url, width=800)
        self.assertIn("w_800", result)

    def test_post_handler_text_extraction(self):
        """Test post handler text extraction methods."""
        mock_client = Mock()
        handler = PostHandler(mock_client)

        # Test extracting text from simple content
        text = handler._extract_text_from_content("Simple text")
        self.assertEqual(text, "Simple text")

        # Test extracting text from dict content
        content = {"type": "text", "content": "Dict text"}
        text = handler._extract_text_from_content(content)
        self.assertEqual(text, "Dict text")


if __name__ == "__main__":
    unittest.main()
