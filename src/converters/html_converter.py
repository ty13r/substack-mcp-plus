# ABOUTME: HTMLConverter class for converting HTML to Substack JSON blocks
# ABOUTME: Uses BeautifulSoup to parse HTML and convert to block format

from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup, NavigableString, Tag
from src.converters.block_builder import BlockBuilder


class HTMLConverter:
    """Converts HTML content to Substack JSON block format"""

    def __init__(self):
        """Initialize the converter with a BlockBuilder instance"""
        self.builder = BlockBuilder()

    def convert(self, html: str) -> List[Dict[str, Any]]:
        """Convert HTML to Substack JSON blocks

        Args:
            html: The HTML content to convert

        Returns:
            A list of Substack JSON blocks
        """
        if not html or not html.strip():
            return []

        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")

        blocks = []

        # Process all top-level elements
        for element in soup.children:
            if isinstance(element, NavigableString):
                # Handle text nodes at the root level
                text = str(element).strip()
                if text:
                    blocks.append(self.builder.paragraph(text))
            else:
                # Process HTML elements
                block = self._process_element(element)
                if block:
                    if isinstance(block, list):
                        blocks.extend(block)
                    else:
                        blocks.append(block)

        return blocks

    def _process_element(self, element: Tag) -> Optional[Any]:
        """Process a single HTML element

        Args:
            element: BeautifulSoup Tag element

        Returns:
            A block dict, list of blocks, or None
        """
        if not element.name:
            return None

        tag_name = element.name.lower()

        # Headers
        if tag_name in ["h1", "h2", "h3", "h4", "h5", "h6"]:
            level = int(tag_name[1])
            text = element.get_text().strip()
            return self.builder.header(text, level)

        # Paragraphs
        elif tag_name == "p":
            content = self._parse_inline_content(element)
            if content:
                return self.builder.paragraph(content)

        # Lists
        elif tag_name == "ul":
            items = []
            for li in element.find_all("li", recursive=False):
                items.append(li.get_text().strip())
            if items:
                return self.builder.unordered_list(items)

        elif tag_name == "ol":
            items = []
            for li in element.find_all("li", recursive=False):
                items.append(li.get_text().strip())
            if items:
                return self.builder.ordered_list(items)

        # Code blocks
        elif tag_name == "pre":
            code_tag = element.find("code")
            if code_tag:
                # Extract language from class if present
                language = ""
                if "class" in code_tag.attrs:
                    for cls in code_tag["class"]:
                        if cls.startswith("language-"):
                            language = cls[9:]  # Remove 'language-' prefix
                            break

                code = code_tag.get_text()
                return self.builder.code_block(code, language)
            else:
                # Pre without code tag
                return self.builder.code_block(element.get_text())

        # Blockquotes
        elif tag_name == "blockquote":
            text = element.get_text().strip()
            return self.builder.blockquote(text)

        # Images
        elif tag_name == "img":
            src = element.get("src", "")
            alt = element.get("alt", "")
            caption = element.get("title", "")
            if src:
                return self.builder.image(src, alt, caption)

        # Horizontal rule
        elif tag_name == "hr":
            return self.builder.horizontal_rule()

        # For other elements, process their children
        else:
            child_blocks = []
            for child in element.children:
                if isinstance(child, NavigableString):
                    text = str(child).strip()
                    if text:
                        child_blocks.append(self.builder.paragraph(text))
                else:
                    child_block = self._process_element(child)
                    if child_block:
                        if isinstance(child_block, list):
                            child_blocks.extend(child_block)
                        else:
                            child_blocks.append(child_block)
            return child_blocks if child_blocks else None

        return None

    def _parse_inline_content(self, element: Tag) -> List[Dict[str, Any]]:
        """Parse inline content with formatting

        Args:
            element: The element to parse

        Returns:
            List of text content with formatting marks
        """
        content = []

        for child in element.children:
            if isinstance(child, NavigableString):
                text = str(child)
                if text:
                    content.append({"type": "text", "content": text})
            else:
                # Handle inline formatting tags
                tag_name = child.name.lower() if child.name else ""
                text = child.get_text()

                if not text:
                    continue

                if tag_name in ["strong", "b"]:
                    # Check for nested formatting
                    nested_content = self._get_nested_marks(child)
                    if nested_content:
                        content.extend(nested_content)
                    else:
                        content.append(self.builder.text(text, ["strong"]))
                elif tag_name in ["em", "i"]:
                    # Check for nested formatting
                    nested_content = self._get_nested_marks(child)
                    if nested_content:
                        content.extend(nested_content)
                    else:
                        content.append(self.builder.text(text, ["em"]))
                elif tag_name == "code":
                    content.append(self.builder.text(text, ["code"]))
                elif tag_name == "a":
                    href = child.get("href", "")
                    if href:
                        content.append(self.builder.link(text, href))
                    else:
                        content.append({"type": "text", "content": text})
                else:
                    # Handle nested formatting more carefully
                    nested_content = self._get_nested_marks(child)
                    if nested_content:
                        content.extend(nested_content)
                    else:
                        content.append({"type": "text", "content": text})

        return content if content else [{"type": "text", "content": ""}]

    def _get_nested_marks(
        self, element: Tag, marks: List[str] = None
    ) -> List[Dict[str, Any]]:
        """Get content with nested formatting marks

        Args:
            element: The element to process
            marks: Accumulated marks from parent elements

        Returns:
            List of text content with appropriate marks
        """
        if marks is None:
            marks = []

        # Add this element's mark if applicable
        tag_name = element.name.lower() if element.name else ""
        current_marks = marks.copy()

        if tag_name in ["strong", "b"] and "strong" not in current_marks:
            current_marks.append("strong")
        elif tag_name in ["em", "i"] and "em" not in current_marks:
            current_marks.append("em")

        content = []

        # Process children
        for child in element.children:
            if isinstance(child, NavigableString):
                text = str(child)
                if text and current_marks:
                    content.append(self.builder.text(text, current_marks))
                elif text:
                    content.append({"type": "text", "content": text})
            else:
                # Recurse for nested elements
                nested = self._get_nested_marks(child, current_marks)
                content.extend(nested)

        return content
