# ABOUTME: Unit tests for BlockBuilder class that creates Substack JSON blocks
# ABOUTME: Tests all block types: paragraph, header, list, code, image, etc.

import pytest
from src.converters.block_builder import BlockBuilder


class TestBlockBuilder:
    """Test suite for BlockBuilder class"""

    def setup_method(self):
        """Set up test fixtures"""
        self.builder = BlockBuilder()

    def test_paragraph_block(self):
        """Test creating a paragraph block"""
        content = "This is a test paragraph."
        block = self.builder.paragraph(content)

        assert block["type"] == "paragraph"
        assert block["content"] == [{"type": "text", "content": content}]

    def test_paragraph_with_formatting(self):
        """Test paragraph with bold, italic, and underline formatting"""
        block = self.builder.paragraph(
            [
                {"type": "text", "content": "Normal "},
                {"type": "text", "content": "bold", "marks": [{"type": "strong"}]},
                {"type": "text", "content": " and "},
                {"type": "text", "content": "italic", "marks": [{"type": "em"}]},
                {"type": "text", "content": " text"},
            ]
        )

        assert block["type"] == "paragraph"
        assert len(block["content"]) == 5
        assert block["content"][1]["marks"][0]["type"] == "strong"
        assert block["content"][3]["marks"][0]["type"] == "em"

    def test_header_blocks(self):
        """Test creating header blocks H1-H6"""
        headers = [
            (1, "heading-one"),
            (2, "heading-two"),
            (3, "heading-three"),
            (4, "heading-four"),
            (5, "heading-five"),
            (6, "heading-six"),
        ]

        for level, expected_type in headers:
            block = self.builder.header("Test Header", level)
            assert block["type"] == expected_type
            assert block["content"] == [{"type": "text", "content": "Test Header"}]

    def test_invalid_header_level(self):
        """Test that invalid header levels raise ValueError"""
        with pytest.raises(ValueError, match="Header level must be between 1 and 6"):
            self.builder.header("Test", 7)

        with pytest.raises(ValueError, match="Header level must be between 1 and 6"):
            self.builder.header("Test", 0)

    def test_unordered_list(self):
        """Test creating an unordered list"""
        items = ["First item", "Second item", "Third item"]
        block = self.builder.unordered_list(items)

        assert block["type"] == "bulleted-list"
        assert len(block["content"]) == 3

        for i, item in enumerate(items):
            assert block["content"][i]["type"] == "bulleted-list-item"
            assert block["content"][i]["content"][0]["type"] == "paragraph"
            assert block["content"][i]["content"][0]["content"][0]["content"] == item

    def test_ordered_list(self):
        """Test creating an ordered list"""
        items = ["Step one", "Step two", "Step three"]
        block = self.builder.ordered_list(items)

        assert block["type"] == "ordered-list"
        assert len(block["content"]) == 3

        for i, item in enumerate(items):
            assert block["content"][i]["type"] == "ordered-list-item"
            assert block["content"][i]["content"][0]["type"] == "paragraph"
            assert block["content"][i]["content"][0]["content"][0]["content"] == item

    def test_code_block(self):
        """Test creating a code block"""
        code = "def hello():\n    print('Hello, World!')"
        block = self.builder.code_block(code, "python")

        assert block["type"] == "code"
        assert block["language"] == "python"
        assert block["content"] == code

    def test_code_block_without_language(self):
        """Test creating a code block without language specification"""
        code = "echo 'Hello, World!'"
        block = self.builder.code_block(code)

        assert block["type"] == "code"
        assert block["language"] == ""
        assert block["content"] == code

    def test_blockquote(self):
        """Test creating a blockquote"""
        quote = "This is a quoted text."
        block = self.builder.blockquote(quote)

        assert block["type"] == "blockquote"
        assert block["content"][0]["type"] == "paragraph"
        assert block["content"][0]["content"][0]["content"] == quote

    def test_image_block(self):
        """Test creating an image block"""
        url = "https://example.com/image.jpg"
        alt_text = "Test image"
        caption = "This is a test image"

        block = self.builder.image(url, alt_text, caption)

        assert block["type"] == "captioned-image"
        assert block["src"] == url
        assert block["alt"] == alt_text
        assert block["caption"] == caption

    def test_image_block_without_caption(self):
        """Test creating an image block without caption"""
        url = "https://example.com/image.jpg"
        alt_text = "Test image"

        block = self.builder.image(url, alt_text)

        assert block["type"] == "captioned-image"
        assert block["src"] == url
        assert block["alt"] == alt_text
        assert block["caption"] == ""

    def test_link_creation(self):
        """Test creating a link within text content"""
        link = self.builder.link("Click here", "https://example.com")

        assert link["type"] == "text"
        assert link["content"] == "Click here"
        assert link["marks"][0]["type"] == "link"
        assert link["marks"][0]["href"] == "https://example.com"

    def test_horizontal_rule(self):
        """Test creating a horizontal rule"""
        block = self.builder.horizontal_rule()

        assert block["type"] == "hr"

    def test_paywall_marker(self):
        """Test creating a paywall marker"""
        block = self.builder.paywall()

        assert block["type"] == "paywall"

    def test_text_with_multiple_marks(self):
        """Test creating text with multiple formatting marks"""
        text = self.builder.text("Bold and italic", ["strong", "em"])

        assert text["type"] == "text"
        assert text["content"] == "Bold and italic"
        assert len(text["marks"]) == 2
        assert {"type": "strong"} in text["marks"]
        assert {"type": "em"} in text["marks"]

    def test_empty_content_handling(self):
        """Test handling of empty content"""
        block = self.builder.paragraph("")
        assert block["content"] == [{"type": "text", "content": ""}]

        block = self.builder.unordered_list([])
        assert block["content"] == []

        block = self.builder.ordered_list([])
        assert block["content"] == []
