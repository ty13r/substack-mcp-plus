# ABOUTME: MarkdownConverter class for converting Markdown text to Substack JSON blocks
# ABOUTME: Uses regex parsing to handle all markdown elements and formatting

import re
from typing import List, Dict, Any, Tuple, Optional
from src.converters.block_builder import BlockBuilder


class MarkdownConverter:
    """Converts Markdown text to Substack JSON block format"""

    def __init__(self):
        """Initialize the converter with a BlockBuilder instance"""
        self.builder = BlockBuilder()

    def convert(self, markdown: str) -> List[Dict[str, Any]]:
        """Convert markdown text to Substack JSON blocks

        Args:
            markdown: The markdown text to convert

        Returns:
            A list of Substack JSON blocks
        """
        if not markdown or not markdown.strip():
            return []

        blocks = []
        lines = markdown.split("\n")
        i = 0

        while i < len(lines):
            line = lines[i]

            # Skip empty lines
            if not line.strip():
                i += 1
                continue

            # Check for code blocks
            if line.strip().startswith("```"):
                block, i = self._parse_code_block(lines, i)
                if block:
                    blocks.append(block)
                continue

            # Check for headers
            if line.startswith("#"):
                block = self._parse_header(line)
                if block:
                    blocks.append(block)
                    i += 1
                    continue

            # Check for horizontal rule
            if re.match(r"^(\-{3,}|\*{3,}|_{3,})$", line.strip()):
                blocks.append(self.builder.horizontal_rule())
                i += 1
                continue

            # Check for blockquote
            if line.startswith(">"):
                block, i = self._parse_blockquote(lines, i)
                if block:
                    blocks.append(block)
                continue

            # Check for lists
            if re.match(r"^(\*|\-|\+|\d+\.) ", line.strip()):
                block, i = self._parse_list(lines, i)
                if block:
                    blocks.append(block)
                continue

            # Default to paragraph
            block, i = self._parse_paragraph(lines, i)
            if block:
                blocks.append(block)

        return blocks

    def _parse_header(self, line: str) -> Optional[Dict[str, Any]]:
        """Parse a header line"""
        match = re.match(r"^(#{1,6})\s+(.+)$", line)
        if match:
            level = len(match.group(1))
            content = match.group(2).strip()
            return self.builder.header(content, level)
        return None

    def _parse_code_block(
        self, lines: List[str], start: int
    ) -> Tuple[Optional[Dict[str, Any]], int]:
        """Parse a code block"""
        line = lines[start].strip()
        if not line.startswith("```"):
            return None, start + 1

        # Extract language if present
        language = line[3:].strip()

        # Find the closing ```
        code_lines = []
        i = start + 1
        while i < len(lines):
            if lines[i].strip() == "```":
                code = "\n".join(code_lines)
                return self.builder.code_block(code, language), i + 1
            code_lines.append(lines[i])
            i += 1

        # If no closing found, treat as paragraph
        return None, start + 1

    def _parse_blockquote(
        self, lines: List[str], start: int
    ) -> Tuple[Optional[Dict[str, Any]], int]:
        """Parse a blockquote"""
        quote_lines = []
        i = start

        while i < len(lines) and lines[i].strip().startswith(">"):
            content = lines[i].strip()[1:].strip()
            quote_lines.append(content)
            i += 1

        if quote_lines:
            quote_text = " ".join(quote_lines)
            return self.builder.blockquote(quote_text), i

        return None, start + 1

    def _parse_list(
        self, lines: List[str], start: int
    ) -> Tuple[Optional[Dict[str, Any]], int]:
        """Parse a list (ordered or unordered)"""
        first_line = lines[start].strip()

        # Determine list type
        is_ordered = bool(re.match(r"^\d+\. ", first_line))

        items = []
        i = start

        # Simple list parsing (not handling nested lists in this version)
        while i < len(lines):
            line = lines[i].strip()

            if not line:
                # Empty line might end the list
                if i + 1 < len(lines) and not re.match(
                    r"^(\*|\-|\+|\d+\.) ", lines[i + 1].strip()
                ):
                    break
                i += 1
                continue

            # Check if this line is a list item
            if is_ordered:
                match = re.match(r"^\d+\. (.+)$", line)
            else:
                match = re.match(r"^(\*|\-|\+) (.+)$", line)

            if match:
                content = match.group(1) if is_ordered else match.group(2)
                items.append(content)
                i += 1
            else:
                break

        if items:
            if is_ordered:
                return self.builder.ordered_list(items), i
            else:
                return self.builder.unordered_list(items), i

        return None, start + 1

    def _parse_paragraph(
        self, lines: List[str], start: int
    ) -> Tuple[Optional[Dict[str, Any]], int]:
        """Parse a paragraph with inline formatting"""
        paragraph_lines = []
        i = start

        while i < len(lines):
            line = lines[i]

            # Stop at empty lines or special syntax
            if (
                not line.strip()
                or line.startswith("#")
                or line.startswith(">")
                or line.strip().startswith("```")
                or re.match(r"^(\*|\-|\+|\d+\.) ", line.strip())
                or re.match(r"^(\-{3,}|\*{3,}|_{3,})$", line.strip())
            ):
                break

            paragraph_lines.append(line)
            i += 1

        if paragraph_lines:
            text = " ".join(paragraph_lines)

            # Check for images first
            img_match = re.match(
                r'^!\[([^\]]*)\]\(([^\s]+)(?:\s+"([^"]+)")?\)$', text.strip()
            )
            if img_match:
                alt_text = img_match.group(1)
                src = img_match.group(2)
                caption = img_match.group(3) or ""
                return self.builder.image(src, alt_text, caption), i

            # Parse inline formatting
            content = self._parse_inline_formatting(text)
            return self.builder.paragraph(content), i

        return None, start + 1

    def _parse_inline_formatting(self, text: str) -> List[Dict[str, Any]]:
        """Parse inline formatting (bold, italic, links, code)"""
        # Handle escaped characters
        text = text.replace("\\*", "\x00ESCAPED_ASTERISK\x00")
        text = text.replace("\\[", "\x00ESCAPED_BRACKET_OPEN\x00")
        text = text.replace("\\]", "\x00ESCAPED_BRACKET_CLOSE\x00")

        elements = []
        remaining = text

        while remaining:
            # Find the next formatting element
            next_match = None
            next_type = None

            patterns = [
                (r"\*\*\*([^*]+)\*\*\*", "bold_italic"),  # ***text***
                (r"\*\*([^*]+)\*\*", "bold"),  # **text**
                (r"\*([^*]+)\*", "italic"),  # *text*
                (r"\[([^\]]+)\]\(([^)]+)\)", "link"),  # [text](url)
                (r"`([^`]+)`", "code"),  # `code`
            ]

            earliest_pos = len(remaining)

            for pattern, format_type in patterns:
                match = re.search(pattern, remaining)
                if match and match.start() < earliest_pos:
                    earliest_pos = match.start()
                    next_match = match
                    next_type = format_type

            if next_match:
                # Add text before the match
                if next_match.start() > 0:
                    plain_text = remaining[: next_match.start()]
                    elements.append(
                        self._restore_escaped_chars(
                            {"type": "text", "content": plain_text}
                        )
                    )

                # Add the formatted element
                if next_type == "bold_italic":
                    elements.append(
                        self._restore_escaped_chars(
                            self.builder.text(next_match.group(1), ["strong", "em"])
                        )
                    )
                elif next_type == "bold":
                    elements.append(
                        self._restore_escaped_chars(
                            self.builder.text(next_match.group(1), ["strong"])
                        )
                    )
                elif next_type == "italic":
                    elements.append(
                        self._restore_escaped_chars(
                            self.builder.text(next_match.group(1), ["em"])
                        )
                    )
                elif next_type == "link":
                    elements.append(
                        self._restore_escaped_chars(
                            self.builder.link(next_match.group(1), next_match.group(2))
                        )
                    )
                elif next_type == "code":
                    elements.append(
                        self._restore_escaped_chars(
                            self.builder.text(next_match.group(1), ["code"])
                        )
                    )

                remaining = remaining[next_match.end() :]
            else:
                # No more formatting, add the rest as plain text
                elements.append(
                    self._restore_escaped_chars({"type": "text", "content": remaining})
                )
                break

        return elements if elements else [{"type": "text", "content": ""}]

    def _restore_escaped_chars(self, element: Dict[str, Any]) -> Dict[str, Any]:
        """Restore escaped characters in text content"""
        if "content" in element and isinstance(element["content"], str):
            element["content"] = element["content"].replace(
                "\x00ESCAPED_ASTERISK\x00", "*"
            )
            element["content"] = element["content"].replace(
                "\x00ESCAPED_BRACKET_OPEN\x00", "["
            )
            element["content"] = element["content"].replace(
                "\x00ESCAPED_BRACKET_CLOSE\x00", "]"
            )
        return element
