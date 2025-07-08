# ABOUTME: Unit tests for MarkdownConverter class that converts Markdown to Substack JSON
# ABOUTME: Tests all markdown elements: headers, lists, code, images, links, etc.

import pytest
from src.converters.markdown_converter import MarkdownConverter


class TestMarkdownConverter:
    """Test suite for MarkdownConverter class"""

    def setup_method(self):
        """Set up test fixtures"""
        self.converter = MarkdownConverter()

    def test_simple_paragraph(self):
        """Test converting a simple paragraph"""
        markdown = "This is a simple paragraph."
        blocks = self.converter.convert(markdown)

        assert len(blocks) == 1
        assert blocks[0]["type"] == "paragraph"
        assert blocks[0]["content"][0]["content"] == "This is a simple paragraph."

    def test_multiple_paragraphs(self):
        """Test converting multiple paragraphs"""
        markdown = "First paragraph.\n\nSecond paragraph.\n\nThird paragraph."
        blocks = self.converter.convert(markdown)

        assert len(blocks) == 3
        for i, block in enumerate(blocks):
            assert block["type"] == "paragraph"

    def test_headers_all_levels(self):
        """Test converting headers H1 through H6"""
        markdown = """# H1 Header
## H2 Header
### H3 Header
#### H4 Header
##### H5 Header
###### H6 Header"""

        blocks = self.converter.convert(markdown)
        expected_types = [
            "heading-one",
            "heading-two",
            "heading-three",
            "heading-four",
            "heading-five",
            "heading-six",
        ]

        assert len(blocks) == 6
        for i, (block, expected_type) in enumerate(zip(blocks, expected_types)):
            assert block["type"] == expected_type
            assert f"H{i+1} Header" in block["content"][0]["content"]

    def test_bold_text(self):
        """Test converting bold text"""
        markdown = "This has **bold text** in it."
        blocks = self.converter.convert(markdown)

        assert len(blocks) == 1
        content = blocks[0]["content"]
        assert len(content) == 3
        assert content[0]["content"] == "This has "
        assert content[1]["content"] == "bold text"
        assert content[1]["marks"][0]["type"] == "strong"
        assert content[2]["content"] == " in it."

    def test_italic_text(self):
        """Test converting italic text"""
        markdown = "This has *italic text* in it."
        blocks = self.converter.convert(markdown)

        assert len(blocks) == 1
        content = blocks[0]["content"]
        assert len(content) == 3
        assert content[1]["content"] == "italic text"
        assert content[1]["marks"][0]["type"] == "em"

    def test_bold_and_italic(self):
        """Test converting text with both bold and italic"""
        markdown = "This has ***bold and italic*** text."
        blocks = self.converter.convert(markdown)

        assert len(blocks) == 1
        content = blocks[0]["content"]
        # Should have both strong and em marks
        assert any("strong" in str(mark) for mark in content[1].get("marks", []))
        assert any("em" in str(mark) for mark in content[1].get("marks", []))

    def test_unordered_list(self):
        """Test converting unordered lists"""
        markdown = """- First item
- Second item
- Third item"""

        blocks = self.converter.convert(markdown)
        assert len(blocks) == 1
        assert blocks[0]["type"] == "bulleted-list"
        assert len(blocks[0]["content"]) == 3

        for i, item in enumerate(blocks[0]["content"]):
            assert item["type"] == "bulleted-list-item"

    def test_ordered_list(self):
        """Test converting ordered lists"""
        markdown = """1. First step
2. Second step
3. Third step"""

        blocks = self.converter.convert(markdown)
        assert len(blocks) == 1
        assert blocks[0]["type"] == "ordered-list"
        assert len(blocks[0]["content"]) == 3

        for item in blocks[0]["content"]:
            assert item["type"] == "ordered-list-item"

    def test_nested_list(self):
        """Test converting nested lists"""
        markdown = """- Parent item
  - Nested item 1
  - Nested item 2
- Another parent"""

        blocks = self.converter.convert(markdown)
        assert len(blocks) == 1
        assert blocks[0]["type"] == "bulleted-list"
        # Nested lists should be flattened or handled appropriately

    def test_code_block_with_language(self):
        """Test converting code blocks with language"""
        markdown = """```python
def hello():
    print("Hello, World!")
```"""

        blocks = self.converter.convert(markdown)
        assert len(blocks) == 1
        assert blocks[0]["type"] == "code"
        assert blocks[0]["language"] == "python"
        assert "def hello():" in blocks[0]["content"]

    def test_code_block_without_language(self):
        """Test converting code blocks without language"""
        markdown = """```
echo "Hello, World!"
```"""

        blocks = self.converter.convert(markdown)
        assert len(blocks) == 1
        assert blocks[0]["type"] == "code"
        assert blocks[0]["language"] == ""
        assert 'echo "Hello, World!"' in blocks[0]["content"]

    def test_inline_code(self):
        """Test converting inline code"""
        markdown = "Use the `print()` function."
        blocks = self.converter.convert(markdown)

        assert len(blocks) == 1
        content = blocks[0]["content"]
        # Inline code should be converted to code marks
        assert any("code" in str(item.get("marks", [])) for item in content)

    def test_blockquote(self):
        """Test converting blockquotes"""
        markdown = "> This is a quote.\n> It has multiple lines."
        blocks = self.converter.convert(markdown)

        assert len(blocks) == 1
        assert blocks[0]["type"] == "blockquote"

    def test_links(self):
        """Test converting links"""
        markdown = "Check out [my website](https://example.com)."
        blocks = self.converter.convert(markdown)

        assert len(blocks) == 1
        content = blocks[0]["content"]
        link_found = False
        for item in content:
            if item.get("marks"):
                for mark in item["marks"]:
                    if (
                        mark.get("type") == "link"
                        and mark.get("href") == "https://example.com"
                    ):
                        link_found = True
                        assert item["content"] == "my website"
        assert link_found

    def test_images(self):
        """Test converting images"""
        markdown = "![Alt text](https://example.com/image.jpg)"
        blocks = self.converter.convert(markdown)

        assert len(blocks) == 1
        assert blocks[0]["type"] == "captioned-image"
        assert blocks[0]["src"] == "https://example.com/image.jpg"
        assert blocks[0]["alt"] == "Alt text"

    def test_images_with_title(self):
        """Test converting images with title (used as caption)"""
        markdown = '![Alt text](https://example.com/image.jpg "Image caption")'
        blocks = self.converter.convert(markdown)

        assert len(blocks) == 1
        assert blocks[0]["type"] == "captioned-image"
        assert blocks[0]["caption"] == "Image caption"

    def test_horizontal_rule(self):
        """Test converting horizontal rules"""
        markdown = "Text above\n\n---\n\nText below"
        blocks = self.converter.convert(markdown)

        assert len(blocks) == 3
        assert blocks[1]["type"] == "hr"

    def test_mixed_content(self):
        """Test converting mixed markdown content"""
        markdown = """# Main Title

This is a paragraph with **bold** and *italic* text.

## Subsection

Here's a list:
- Item 1
- Item 2

```python
code_example = True
```

> A thoughtful quote

Check [this link](https://example.com) for more info."""

        blocks = self.converter.convert(markdown)

        # Verify we have all the expected block types
        block_types = [block["type"] for block in blocks]
        assert "heading-one" in block_types
        assert "heading-two" in block_types
        assert "paragraph" in block_types
        assert "bulleted-list" in block_types
        assert "code" in block_types
        assert "blockquote" in block_types

    def test_empty_input(self):
        """Test converting empty markdown"""
        blocks = self.converter.convert("")
        assert blocks == []

    def test_whitespace_only(self):
        """Test converting whitespace-only markdown"""
        blocks = self.converter.convert("   \n\n   \n")
        assert blocks == []

    def test_special_characters_escaping(self):
        """Test that special characters are properly handled"""
        markdown = "This has \\*escaped asterisks\\* and \\[escaped brackets\\]"
        blocks = self.converter.convert(markdown)

        assert len(blocks) == 1
        content = blocks[0]["content"][0]["content"]
        assert "*escaped asterisks*" in content
        assert "[escaped brackets]" in content
