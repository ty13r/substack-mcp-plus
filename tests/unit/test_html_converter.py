# ABOUTME: Unit tests for HTMLConverter class that converts HTML to Substack JSON
# ABOUTME: Tests all HTML elements: headers, paragraphs, lists, images, links, etc.

import pytest
from src.converters.html_converter import HTMLConverter


class TestHTMLConverter:
    """Test suite for HTMLConverter class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.converter = HTMLConverter()
    
    def test_simple_paragraph(self):
        """Test converting a simple paragraph"""
        html = "<p>This is a simple paragraph.</p>"
        blocks = self.converter.convert(html)
        
        assert len(blocks) == 1
        assert blocks[0]["type"] == "paragraph"
        assert blocks[0]["content"][0]["content"] == "This is a simple paragraph."
    
    def test_multiple_paragraphs(self):
        """Test converting multiple paragraphs"""
        html = "<p>First paragraph.</p><p>Second paragraph.</p><p>Third paragraph.</p>"
        blocks = self.converter.convert(html)
        
        assert len(blocks) == 3
        for block in blocks:
            assert block["type"] == "paragraph"
    
    def test_headers_all_levels(self):
        """Test converting headers H1 through H6"""
        html = """<h1>H1 Header</h1>
<h2>H2 Header</h2>
<h3>H3 Header</h3>
<h4>H4 Header</h4>
<h5>H5 Header</h5>
<h6>H6 Header</h6>"""
        
        blocks = self.converter.convert(html)
        expected_types = [
            "heading-one", "heading-two", "heading-three",
            "heading-four", "heading-five", "heading-six"
        ]
        
        assert len(blocks) == 6
        for i, (block, expected_type) in enumerate(zip(blocks, expected_types)):
            assert block["type"] == expected_type
            assert f"H{i+1} Header" in block["content"][0]["content"]
    
    def test_bold_text(self):
        """Test converting bold text"""
        html = "<p>This has <strong>bold text</strong> in it.</p>"
        blocks = self.converter.convert(html)
        
        assert len(blocks) == 1
        content = blocks[0]["content"]
        assert len(content) == 3
        assert content[0]["content"] == "This has "
        assert content[1]["content"] == "bold text"
        assert content[1]["marks"][0]["type"] == "strong"
        assert content[2]["content"] == " in it."
    
    def test_italic_text(self):
        """Test converting italic text"""
        html = "<p>This has <em>italic text</em> in it.</p>"
        blocks = self.converter.convert(html)
        
        assert len(blocks) == 1
        content = blocks[0]["content"]
        assert len(content) == 3
        assert content[1]["content"] == "italic text"
        assert content[1]["marks"][0]["type"] == "em"
    
    def test_nested_formatting(self):
        """Test nested bold and italic"""
        html = "<p>This has <strong><em>bold and italic</em></strong> text.</p>"
        blocks = self.converter.convert(html)
        
        assert len(blocks) == 1
        content = blocks[0]["content"]
        # Should have both strong and em marks
        formatted_text = next(item for item in content if item.get("marks"))
        marks = [mark["type"] for mark in formatted_text.get("marks", [])]
        assert "strong" in marks
        assert "em" in marks
    
    def test_unordered_list(self):
        """Test converting unordered lists"""
        html = """<ul>
<li>First item</li>
<li>Second item</li>
<li>Third item</li>
</ul>"""
        
        blocks = self.converter.convert(html)
        assert len(blocks) == 1
        assert blocks[0]["type"] == "bulleted-list"
        assert len(blocks[0]["content"]) == 3
        
        for item in blocks[0]["content"]:
            assert item["type"] == "bulleted-list-item"
    
    def test_ordered_list(self):
        """Test converting ordered lists"""
        html = """<ol>
<li>First step</li>
<li>Second step</li>
<li>Third step</li>
</ol>"""
        
        blocks = self.converter.convert(html)
        assert len(blocks) == 1
        assert blocks[0]["type"] == "ordered-list"
        assert len(blocks[0]["content"]) == 3
        
        for item in blocks[0]["content"]:
            assert item["type"] == "ordered-list-item"
    
    def test_code_blocks(self):
        """Test converting code blocks"""
        html = '<pre><code>def hello():\n    print("Hello!")</code></pre>'
        blocks = self.converter.convert(html)
        
        assert len(blocks) == 1
        assert blocks[0]["type"] == "code"
        assert "def hello():" in blocks[0]["content"]
    
    def test_code_with_language(self):
        """Test code blocks with language class"""
        html = '<pre><code class="language-python">def hello():\n    pass</code></pre>'
        blocks = self.converter.convert(html)
        
        assert len(blocks) == 1
        assert blocks[0]["type"] == "code"
        assert blocks[0]["language"] == "python"
    
    def test_blockquote(self):
        """Test converting blockquotes"""
        html = "<blockquote>This is a quote.</blockquote>"
        blocks = self.converter.convert(html)
        
        assert len(blocks) == 1
        assert blocks[0]["type"] == "blockquote"
    
    def test_links(self):
        """Test converting links"""
        html = '<p>Check out <a href="https://example.com">my website</a>.</p>'
        blocks = self.converter.convert(html)
        
        assert len(blocks) == 1
        content = blocks[0]["content"]
        link_found = False
        for item in content:
            if item.get("marks"):
                for mark in item["marks"]:
                    if mark.get("type") == "link" and mark.get("href") == "https://example.com":
                        link_found = True
                        assert item["content"] == "my website"
        assert link_found
    
    def test_images(self):
        """Test converting images"""
        html = '<img src="https://example.com/image.jpg" alt="Alt text">'
        blocks = self.converter.convert(html)
        
        assert len(blocks) == 1
        assert blocks[0]["type"] == "captioned-image"
        assert blocks[0]["src"] == "https://example.com/image.jpg"
        assert blocks[0]["alt"] == "Alt text"
    
    def test_images_with_title(self):
        """Test converting images with title attribute"""
        html = '<img src="https://example.com/image.jpg" alt="Alt text" title="Image caption">'
        blocks = self.converter.convert(html)
        
        assert len(blocks) == 1
        assert blocks[0]["type"] == "captioned-image"
        assert blocks[0]["caption"] == "Image caption"
    
    def test_horizontal_rule(self):
        """Test converting horizontal rules"""
        html = "<p>Text above</p><hr><p>Text below</p>"
        blocks = self.converter.convert(html)
        
        assert len(blocks) == 3
        assert blocks[1]["type"] == "hr"
    
    def test_mixed_content(self):
        """Test converting mixed HTML content"""
        html = """<h1>Main Title</h1>
<p>This is a paragraph with <strong>bold</strong> and <em>italic</em> text.</p>
<h2>Subsection</h2>
<p>Here's a list:</p>
<ul>
<li>Item 1</li>
<li>Item 2</li>
</ul>
<pre><code>code_example = True</code></pre>
<blockquote>A thoughtful quote</blockquote>
<p>Check <a href="https://example.com">this link</a> for more info.</p>"""
        
        blocks = self.converter.convert(html)
        
        # Verify we have all the expected block types
        block_types = [block["type"] for block in blocks]
        assert "heading-one" in block_types
        assert "heading-two" in block_types
        assert "paragraph" in block_types
        assert "bulleted-list" in block_types
        assert "code" in block_types
        assert "blockquote" in block_types
    
    def test_empty_input(self):
        """Test converting empty HTML"""
        blocks = self.converter.convert("")
        assert blocks == []
    
    def test_whitespace_only(self):
        """Test converting whitespace-only HTML"""
        blocks = self.converter.convert("   \n\n   \n")
        assert blocks == []
    
    def test_malformed_html(self):
        """Test handling malformed HTML"""
        html = "<p>Unclosed paragraph"
        blocks = self.converter.convert(html)
        # Should still parse what it can
        assert len(blocks) == 1
        assert blocks[0]["type"] == "paragraph"
    
    def test_nested_lists(self):
        """Test nested lists get flattened"""
        html = """<ul>
<li>Parent item
  <ul>
    <li>Nested item</li>
  </ul>
</li>
</ul>"""
        
        blocks = self.converter.convert(html)
        # Nested lists should be handled appropriately
        assert len(blocks) >= 1
        assert blocks[0]["type"] == "bulleted-list"