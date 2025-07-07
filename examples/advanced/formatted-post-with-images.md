# Advanced Example: Rich Text Post with Images

This example demonstrates creating a fully formatted post with headers, lists, code blocks, and images.

## Example Conversation

**You:** Create a draft post about "Building with AI Tools" with the following content:

```
# Building with AI Tools

## Introduction

I've been exploring how AI can accelerate software development. Here's what I've learned.

### Key Benefits:
- **Faster prototyping** - Go from idea to working code in hours
- **Better documentation** - AI helps write comprehensive docs
- **Test-driven development** - AI can write tests first

## Code Example

Here's a simple Python function:

```python
def hello_ai():
    return "Hello from AI-assisted coding!"
```

## My Setup

1. Claude Desktop for coding
2. GitHub Copilot for autocomplete
3. ChatGPT for research

> "AI doesn't replace developers, it amplifies them" - Every tech blog in 2024

## Conclusion

The future is collaborative: humans and AI working together.
```

**Claude will:**
1. Parse the Markdown formatting
2. Convert to Substack's format (headers, lists, code blocks)
3. Create a rich text draft

## Adding Images

**You:** Upload an image from my desktop at /Users/me/screenshot.png and add it to the post

**Claude will:**
1. Use `upload_image` tool to upload to Substack CDN
2. Get the image URL
3. Use `update_post` to add the image to your draft

## Publishing with Custom Settings

**You:** Schedule this post for next Monday at 9 AM EST

**Claude will:**
1. Use `schedule_post` with the post ID
2. Set publication date/time
3. Confirm scheduling

## Advanced Formatting Tips

- Use `---` for horizontal rules
- Wrap code with triple backticks for syntax highlighting
- Use `>` for blockquotes
- Headers (H1-H6) are supported with #
- Tables work with pipe syntax
- Links: `[text](url)` format