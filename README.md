# Substack MCP Plus

[![npm version](https://img.shields.io/npm/v/substack-mcp-plus.svg)](https://www.npmjs.com/package/substack-mcp-plus)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io)

**The most advanced Substack MCP server available.** Create publication-ready posts with full rich text formatting, manage drafts, schedule posts, and more - all from Claude Desktop or any MCP-compatible client.

## 🌟 Why Choose Substack MCP Plus?

> **[See detailed feature comparison →](docs/FEATURES.md)**

### ✨ Seamless Authentication
- **Browser-based setup** - No API keys or complex configuration
- **CAPTCHA support** - Handles security challenges automatically  
- **Secure token storage** - Encrypted local storage, no passwords in configs
- **Magic link & password auth** - Works with any Substack account type

### 📝 Unmatched Content Creation
- **Full rich text support** - Headers, bold, italic, lists, code blocks, images
- **Multiple formats** - Write in Markdown, HTML, or plain text
- **Smart formatting** - Automatic conversion to Substack's native format
- **Paywall markers** - Easily separate free and premium content

### 🎯 14 Powerful Tools
Create, update, publish, schedule, duplicate posts and more. The most comprehensive Substack automation toolkit available.

### 🚀 Zero-Config Setup
```bash
npm install -g substack-mcp-plus
```
That's it! Automatic Python detection, virtual environment setup, and dependency installation.

## 💭 Why We Built This

> "So many ideas, little time to actually publish them."

I'm a product guy with countless ideas swirling in my head. Before LLMs, writing was the bottleneck. Now with Claude and ChatGPT producing detailed articles in minutes, I realized **publishing had become the new constraint**.

### The Journey

After spending 2-3 frustrating hours trying to set up an existing Substack MCP server (involving stealing session tokens from browser dev tools!), we finally got it working. We were ecstatic... until we tried to publish our first post.

**All formatting was gone. Plain text only.**

Our hopes were crushed, but from that disappointment came determination. Why hadn't anyone built on the battle-tested `python-substack` library? This was our opportunity.

### The Experiment

As someone who hadn't written production code since 2018, I wanted to test a theory: **Could AI agents build production-quality software with proper planning and TDD?**

The answer was a resounding yes. Using Claude Code with strict Test-Driven Development:
- Write failing tests first
- Implement code to pass those tests
- No hallucinations, no massive errors
- I was "the equivalent of Homer Simpson running the nuclear power plant"

**The result?** In under 24 hours, we built the most powerful Substack MCP server available. **And I didn't write a single line of code.**

### Our Vision

This isn't just about one tool. It's about:
- **Empowering creators** to ship ideas without friction
- **Inspiring developers** to build on this foundation
- **Proving what's possible** with AI-assisted development
- **Setting the standard** for what publishing automation should be

Because when publishing is frictionless, ideas flow freely.

**[→ Read our full vision and roadmap](docs/VISION.md)**

## 📚 Documentation

For detailed guides and documentation, see the [docs directory](docs/):
- **[Quick Start Guide](QUICKSTART.md)** - Get up and running in 5 minutes
- **[Authentication Guide](docs/authentication.md)** - Detailed setup instructions
- **[Formatting Guide](docs/formatting.md)** - All supported formatting options with examples
- **[Testing Guide](docs/testing_guide.md)** - Comprehensive testing instructions
- **[All Documentation](docs/)** - Complete documentation index

## 🛠 Available Tools

All 14 tools at a glance:
1. **create_formatted_post** - Create rich text drafts
2. **update_post** - Edit existing drafts
3. **publish_post** - Publish immediately
4. **schedule_post** - Schedule for future
5. **list_drafts** - View draft posts
6. **list_published** - View published posts
7. **get_post_content** - Read full post content
8. **duplicate_post** - Copy existing posts
9. **upload_image** - Upload to Substack CDN
10. **preview_draft** - Generate preview links
11. **get_sections** - List publication sections
12. **get_subscriber_count** - View subscriber stats
13. **delete_draft** - Remove drafts safely
14. **list_drafts_for_deletion** - Bulk draft management

### Core Tools

<details>
<summary><strong>create_formatted_post</strong> - Create a draft post with rich formatting</summary>

**Inputs**:
- `title` (string, required): Title of the post
- `content` (string, required): Content of the post (Markdown, HTML, or plain text)
- `subtitle` (string, optional): Subtitle of the post
- `content_type` (string, optional): Format of content - "markdown" (default), "html", or "plain"

**Returns**: Post details including ID, title, subtitle, and URL

**Example**:
```markdown
# My Amazing Post

This post has **bold** text, *italics*, and even code:

```python
def hello():
    print("Hello, Substack!")
```

- Bullet points
- With multiple items

> And blockquotes too!
```
</details>

<details>
<summary><strong>update_post</strong> - Update an existing draft</summary>

**Inputs**:
- `post_id` (string, required): ID of the post to update
- `title` (string, optional): New title
- `content` (string, optional): New content
- `subtitle` (string, optional): New subtitle
- `content_type` (string, optional): Format of content if provided

**Returns**: Updated post details
</details>

<details>
<summary><strong>publish_post</strong> - Publish a draft immediately</summary>

**Inputs**:
- `post_id` (string, required): ID of the draft to publish

**Returns**: Published post details
</details>

<details>
<summary><strong>schedule_post</strong> - Schedule a draft for future publication</summary>

**Inputs**:
- `post_id` (string, required): ID of the draft to schedule
- `scheduled_at` (string, required): ISO 8601 datetime when to publish (e.g., '2024-01-15T10:00:00Z')

**Returns**: Scheduled post details
</details>

### Content Management

<details>
<summary><strong>list_drafts</strong> - List recent draft posts</summary>

**Inputs**:
- `limit` (integer, optional): Maximum number of drafts to return (1-25, default: 10)

**Returns**: List of drafts with metadata
</details>

<details>
<summary><strong>list_published</strong> - List recently published posts</summary>

**Inputs**:
- `limit` (integer, optional): Maximum number of posts to return (1-25, default: 10)

**Returns**: List of published posts with titles, IDs, and publication dates
</details>

<details>
<summary><strong>get_post_content</strong> - Read the full content of any post</summary>

**Inputs**:
- `post_id` (string, required): ID of the post to read

**Returns**: Complete post content in readable markdown format
</details>

<details>
<summary><strong>duplicate_post</strong> - Create a copy of an existing post</summary>

**Inputs**:
- `post_id` (string, required): ID of the post to duplicate
- `new_title` (string, optional): Title for the copy (defaults to "Copy of [original]")

**Returns**: New draft post with duplicated content
</details>

### Media & Resources

<details>
<summary><strong>upload_image</strong> - Upload an image to Substack's CDN</summary>

**Inputs**:
- `image_path` (string, required): Full path to the image file

**Returns**: URL for the uploaded image
</details>

<details>
<summary><strong>preview_draft</strong> - Generate a shareable preview link</summary>

**Inputs**:
- `post_id` (string, required): ID of the draft to preview

**Returns**: Preview link that can be shared for feedback
</details>

### Publication Management

<details>
<summary><strong>get_sections</strong> - List available sections/categories</summary>

**Inputs**: None

**Returns**: List of sections with IDs and names
</details>

<details>
<summary><strong>get_subscriber_count</strong> - Get total subscriber count</summary>

**Inputs**: None

**Returns**: Total number of subscribers and publication URL
</details>

### Housekeeping

<details>
<summary><strong>delete_draft</strong> - Safely delete a draft post</summary>

**Inputs**:
- `post_id` (string, required): ID of the draft to delete
- `confirm_delete` (boolean, required): Must be true to confirm deletion

**Returns**: Confirmation of deletion
</details>

<details>
<summary><strong>list_drafts_for_deletion</strong> - List drafts with detailed info for bulk management</summary>

**Inputs**:
- `limit` (integer, optional): Maximum number of drafts to return (1-25, default: 25)

**Returns**: Detailed list of drafts with IDs, titles, and last updated dates
</details>

## 📋 Requirements

- Python 3.9 or higher
- Substack account credentials:
    - Email and password (recommended)
    - OR session token and user ID
- An LLM client that supports Model Context Protocol (MCP)

## 🔒 Security Best Practices

### Protecting Your Credentials

1. **Never commit your `.env` file** to version control
   - Use the provided `.env.example` as a template
   - Create your own `.env` file with your actual credentials
   - The `.env` file is already in `.gitignore` for your protection

2. **Use strong, unique passwords**
   - Don't reuse your Substack password elsewhere
   - Consider using a password manager
   - Enable two-factor authentication on your Substack account if available

3. **Rotate credentials regularly**
   - Change your Substack password periodically
   - If using session tokens, refresh them when they expire
   - Immediately change credentials if you suspect they've been compromised

### Secure Configuration

When configuring your MCP client:
- Store credentials in environment variables, not in code
- Use the most restrictive file permissions for configuration files
- Avoid logging or printing credentials
- Be cautious when sharing configuration examples

### Reporting Security Issues

Found a security vulnerability? Please **DO NOT** create a public issue. Instead:
1. Check our [SECURITY.md](SECURITY.md) file for reporting guidelines
2. Report privately to maintain responsible disclosure
3. Allow time for a fix before public disclosure

For more security information, see our [Security Policy](SECURITY.md).

## 🔧 Installation

### 1. Install the package
```bash
npm install -g substack-mcp-plus
```

This automatically:
- ✅ Detects Python 3.10+ on your system
- ✅ Creates a Python virtual environment
- ✅ Installs all dependencies
- ✅ Sets up the `substack-mcp-plus` command

### 2. Authenticate with Substack
```bash
cd $(npm root -g)/substack-mcp-plus
python setup_auth.py
```

The interactive wizard will:
- Open a browser for secure login
- Handle CAPTCHA challenges
- Store encrypted credentials
- Test your connection

### 3. Configure Claude Desktop
Add to your Claude Desktop configuration:

```json
{
  "mcpServers": {
    "substack-mcp-plus": {
      "command": "substack-mcp-plus",
      "env": {
        "SUBSTACK_PUBLICATION_URL": "https://yourpublication.substack.com"
      }
    }
  }
}
```

**That's it!** No API keys, no token management, just seamless integration.

## 🎨 Formatting Examples

### Headers and Text Styling
```markdown
# Main Title (H1)
## Section Header (H2)
### Subsection (H3)

Regular text with **bold**, *italic*, and ***bold italic*** formatting.
```

### Lists
```markdown
Unordered list:
- First item
- Second item
- Third item

Ordered list:
1. First step
2. Second step
3. Third step
```

### Code Blocks
````markdown
```python
def greet(name):
    return f"Hello, {name}!"
```
````

### Links and Images
```markdown
[Visit my website](https://example.com)

![Alt text](https://example.com/image.jpg "Optional caption")
```

### Paywall Marker
```markdown
Free content here...

<!--paywall-->

Premium content here...
```

## 🧪 Development

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/unit/test_markdown_converter.py
```

### Code Formatting
```bash
# Format code
black src tests

# Type checking
mypy src
```

## 📦 Project Structure

```
substack-mcp-plus/
├── src/
│   ├── converters/      # Format converters (Markdown → Substack JSON)
│   ├── handlers/        # API handlers (auth, posts, images)
│   ├── tools/           # MCP tool implementations
│   └── server.py        # Main MCP server
├── tests/
│   ├── unit/           # Unit tests for components
│   └── integration/    # End-to-end workflow tests
└── pyproject.toml      # Project configuration
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Write tests for your changes
4. Implement your feature
5. Run tests to ensure everything passes
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Original [substack-mcp](https://github.com/marcomoauro/substack-mcp) by Marco Moauro
- [python-substack](https://github.com/mit1280/python-substack) library
- Model Context Protocol specification

## 📝 Known Limitations

- **Text formatting** (bold/italic) displays as markdown syntax (`**bold**`, `*italic*`) rather than formatted text
- **Links** display as markdown syntax (`[text](url)`) rather than clickable links
- **Blockquotes** display with `>` prefix rather than styled blocks
- Rate limiting is not implemented (be mindful of Substack's API limits)
- No support for collaborative posts
- No analytics data access

**Note**: We use a safe approach that prioritizes reliable content display over advanced formatting. All content will always display correctly, though some formatting may appear as plain text with markdown syntax.

## 🆘 Support

- For issues: Open an issue on [GitHub](https://github.com/your-username/substack-mcp-plus/issues)
- For questions: Start a discussion in the [Discussions](https://github.com/your-username/substack-mcp-plus/discussions) tab