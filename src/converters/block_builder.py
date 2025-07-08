# ABOUTME: BlockBuilder class for creating Substack JSON block format
# ABOUTME: Provides methods to create all supported block types with proper structure

from typing import List, Dict, Any, Optional, Union


class BlockBuilder:
    """Builder class for creating Substack JSON blocks"""

    def paragraph(self, content: Union[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """Create a paragraph block

        Args:
            content: Either a string or a list of text objects with formatting

        Returns:
            A paragraph block dictionary
        """
        if isinstance(content, str):
            content = [{"type": "text", "content": content}]

        return {"type": "paragraph", "content": content}

    def header(self, content: str, level: int) -> Dict[str, Any]:
        """Create a header block

        Args:
            content: The header text
            level: Header level (1-6)

        Returns:
            A header block dictionary

        Raises:
            ValueError: If level is not between 1 and 6
        """
        if level < 1 or level > 6:
            raise ValueError("Header level must be between 1 and 6")

        header_types = {
            1: "heading-one",
            2: "heading-two",
            3: "heading-three",
            4: "heading-four",
            5: "heading-five",
            6: "heading-six",
        }

        return {
            "type": header_types[level],
            "content": [{"type": "text", "content": content}],
        }

    def unordered_list(self, items: List[str]) -> Dict[str, Any]:
        """Create an unordered (bulleted) list

        Args:
            items: List of item strings

        Returns:
            A bulleted list block dictionary
        """
        content = []
        for item in items:
            content.append(
                {"type": "bulleted-list-item", "content": [self.paragraph(item)]}
            )

        return {"type": "bulleted-list", "content": content}

    def ordered_list(self, items: List[str]) -> Dict[str, Any]:
        """Create an ordered (numbered) list

        Args:
            items: List of item strings

        Returns:
            An ordered list block dictionary
        """
        content = []
        for item in items:
            content.append(
                {"type": "ordered-list-item", "content": [self.paragraph(item)]}
            )

        return {"type": "ordered-list", "content": content}

    def code_block(self, code: str, language: str = "") -> Dict[str, Any]:
        """Create a code block

        Args:
            code: The code content
            language: Optional language identifier

        Returns:
            A code block dictionary
        """
        return {"type": "code", "language": language, "content": code}

    def blockquote(self, content: str) -> Dict[str, Any]:
        """Create a blockquote

        Args:
            content: The quote text

        Returns:
            A blockquote block dictionary
        """
        return {"type": "blockquote", "content": [self.paragraph(content)]}

    def image(self, src: str, alt: str, caption: str = "") -> Dict[str, Any]:
        """Create an image block

        Args:
            src: The image URL
            alt: Alternative text for the image
            caption: Optional caption

        Returns:
            An image block dictionary
        """
        return {"type": "captioned-image", "src": src, "alt": alt, "caption": caption}

    def link(self, text: str, href: str) -> Dict[str, Any]:
        """Create a link text object

        Args:
            text: The link text
            href: The link URL

        Returns:
            A text object with link mark
        """
        return {
            "type": "text",
            "content": text,
            "marks": [{"type": "link", "href": href}],
        }

    def horizontal_rule(self) -> Dict[str, Any]:
        """Create a horizontal rule

        Returns:
            A horizontal rule block dictionary
        """
        return {"type": "hr"}

    def paywall(self) -> Dict[str, Any]:
        """Create a paywall marker

        Returns:
            A paywall block dictionary
        """
        return {"type": "paywall"}

    def text(self, content: str, marks: Optional[List[str]] = None) -> Dict[str, Any]:
        """Create a text object with optional formatting marks

        Args:
            content: The text content
            marks: Optional list of mark types (e.g., ["strong", "em"])

        Returns:
            A text object dictionary
        """
        text_obj = {"type": "text", "content": content}

        if marks:
            text_obj["marks"] = [{"type": mark} for mark in marks]

        return text_obj
