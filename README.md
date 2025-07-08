# Substack MCP Plus

[![npm version](https://img.shields.io/npm/v/substack-mcp-plus.svg)](https://www.npmjs.com/package/substack-mcp-plus)
[![npm downloads](https://img.shields.io/npm/dm/substack-mcp-plus.svg)](https://www.npmjs.com/package/substack-mcp-plus)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org)
[![Tests](https://github.com/ty13r/substack-mcp-plus/actions/workflows/ci.yml/badge.svg)](https://github.com/ty13r/substack-mcp-plus/actions/workflows/ci.yml)

**The most advanced Substack MCP server available.** Create publication-ready posts in minutes with full rich text formatting, manage drafts, schedule posts, and more - all from [Claude Desktop](https://claude.ai/download) or any MCP-compatible client.

## 📋 Requirements

- Python 3.10 or higher
- Substack account credentials:
    - Email and password (recommended)
    - OR session token and user ID
- An LLM client that supports Model Context Protocol (MCP)
    - This MCP server has been thoroughly tested with Claude Desktop

## ⚠️ Important Disclaimers

**This is an UNOFFICIAL tool** with no affiliation to Substack Inc.
- We are not endorsed by or associated with Substack
- This tool uses the unofficial [python-substack](https://github.com/ma2za/python-substack) library
- Substack does not provide a public API; this tool uses reverse-engineered endpoints
- Functionality may break if Substack changes their private API
- Use at your own risk and in accordance with Substack's Terms of Service

**[→ See all known issues and limitations](docs/KNOWN_ISSUES.md)**

## 🚀 Zero-Config Setup

### 1. Install the package
```bash
npm install -g substack-mcp-plus
```

### 2. Authenticate with Substack
```bash
substack-mcp-plus-setup
```

The setup wizard will:
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

That's it! Automatic Python detection, virtual environment setup, and dependency installation.

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

### ⚡ Lightning-Fast Publishing
- **30 seconds to draft** - "Create a post about X" → Draft ready in Substack
- **Instant publishing** - "Publish my latest draft" → Live to subscribers
- **No context switching** - Write, edit, and publish without leaving Claude Desktop
- **Bulk operations** - Create multiple posts in minutes, not hours
- **From idea to published** - What used to take 30-60 minutes now takes 2-3 minutes

### 🎯 12 Powerful Tools
Create, update, publish, duplicate posts and more. The most comprehensive Substack automation toolkit available.

## 🛠 Available Tools

All 12 tools at a glance:
1. **create_formatted_post** - Create rich text drafts
2. **update_post** - Edit existing drafts  
3. **publish_post** - Publish immediately
4. **list_drafts** - View draft posts
5. **list_published** - View published posts
6. **get_post_content** - Read full post content
7. **duplicate_post** - Copy existing posts
8. **upload_image** - Upload to Substack CDN
9. **preview_draft** - Generate preview links
10. **get_sections** - List publication sections
11. **get_subscriber_count** - View subscriber stats
12. **delete_draft** - Remove drafts safely

## 💬 Examples of What to Expect

Here's what you can say to Claude Desktop and what each tool will do:

### Creating Content
**You say:** "Create a new Substack draft about AI and the future of work"  
**What happens:** Creates a draft post with your content, returns the post ID and URL  
**Claude shows:** "I've created a draft post titled 'AI and the Future of Work' (ID: 123456)"

**You say:** "Write a post with a paywall after the introduction"  
**What happens:** Creates a draft with free preview content and premium content separated by `<!--paywall-->`  
**Claude shows:** "Draft created with paywall marker. Free readers will see the intro, subscribers get full access."

### Managing Posts
**You say:** "Show me my last 5 drafts"  
**What happens:** Lists your most recent draft posts with titles, IDs, and dates  
**Claude shows:** A formatted list like:
```
1. "AI and the Future of Work" (ID: 123456) - Created 2 hours ago
2. "Weekly Newsletter #42" (ID: 123455) - Created yesterday
3. "Book Review: Deep Work" (ID: 123454) - Created 3 days ago
```

**You say:** "Update the subtitle of draft 123456 to 'How automation will reshape careers'"  
**What happens:** Updates only the subtitle field of the specified draft  
**Claude shows:** "Updated post subtitle. Note: This replaces the entire subtitle field."

**You say:** "Publish my latest draft"  
**What happens:** Publishes the draft immediately to your subscribers  
**Claude shows:** "Post published! It's now live at: https://yourpub.substack.com/p/ai-and-future-work"

### Working with Content
**You say:** "Show me what's in my published post about remote work"  
**What happens:** Retrieves and displays the full formatted content of the post  
**Claude shows:** The complete post content in readable markdown format

**You say:** "Make a copy of my most popular post to use as a template"  
**What happens:** Creates a new draft with identical content but titled "Copy of [original]"  
**Claude shows:** "Created draft 'Copy of Your Popular Post' (ID: 123457)"

**You say:** "Upload the chart image from my desktop"  
**What happens:** Uploads the image to Substack's CDN and returns the URL  
**Claude shows:** "Image uploaded successfully: https://substackcdn.com/image/..."

### Analytics & Management
**You say:** "How many subscribers do I have?"  
**What happens:** Retrieves your current subscriber count  
**Claude shows:** "You have 1,234 subscribers on https://yourpub.substack.com"

**You say:** "What sections does my publication have?"  
**What happens:** Lists all your publication's sections/categories  
**Claude shows:** "Your publication has these sections: Newsletter, Essays, Book Reviews, Podcast"

**You say:** "Generate a preview link for draft 123456"  
**What happens:** Creates an author-only preview URL for sharing  
**Claude shows:** "Preview link: https://yourpub.substack.com/p/ai-and-future-work?preview=true"

**You say:** "Delete that test draft I created earlier"  
**What happens:** Asks for confirmation, then permanently deletes the draft  
**Claude shows:** "Are you sure you want to delete 'Test Post'? Please confirm."

### Important Notes
- All formatting (bold, italic, lists, code blocks) is preserved when creating posts
- The tool handles authentication automatically - no manual token management needed
- Draft posts are saved instantly and can be edited in Substack's web editor too
- Published posts go live immediately to all your subscribers

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

**[→ Read our full vision](docs/VISION.md)** | **[→ See the development roadmap](docs/ROADMAP.md)**

## 📚 Documentation

For detailed guides and documentation, see the [docs directory](docs/):
- **[Quick Start Guide](docs/QUICKSTART.md)** - Get up and running in 5 minutes
- **[Authentication Guide](docs/authentication.md)** - Detailed setup instructions
- **[Formatting Guide](docs/formatting.md)** - All supported formatting options with examples
- **[Testing Guide](docs/testing_guide.md)** - Comprehensive testing instructions
- **[All Documentation](docs/)** - Complete documentation index

## 📝 Known Limitations

**[→ See detailed documentation in KNOWN_ISSUES.md](docs/KNOWN_ISSUES.md)**

### Formatting & Display
- **Text formatting** shows as markdown syntax (`**bold**`, `*italic*`) instead of formatted text
- **Links** display as `[text](url)` instead of clickable links  
- **Images** may show as `![alt](url)` instead of rendered images
- **Blockquotes** display with `>` prefix instead of styled blocks

### API & Feature Limitations
- **No rate limiting** - be mindful of Substack's undocumented API limits
- **Subscriber count** may show 0 even with active subscribers (API limitation)
- **Post scheduling removed** in v1.0.3 due to outdated API endpoint (404 errors)
- **Preview links** are author-only (shareable links require UUID access not available)

### Unsupported Features
- No collaborative posts, threads, or podcast episodes
- No analytics beyond subscriber count (views, opens, engagement)
- No custom CSS, JavaScript, or embedded content (tweets, videos)
- Maximum post size limits are undocumented

### Technical Constraints
- Uses **unofficial reverse-engineered API** that may change without notice
- **python-substack library** hasn't been updated in 2+ years
- Session tokens expire and require re-authentication
- Some accounts with advanced security may have issues

**Workaround**: Create drafts with this tool, then use Substack's web editor for final formatting touches before publishing.

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

We welcome contributions! Check out:
- **[Current TODOs](docs/TODO.md)** - Specific tasks you can claim and work on
- **[Contributing Guide](CONTRIBUTING.md)** - Detailed contribution guidelines
- **[Roadmap](docs/ROADMAP.md)** - Future features and vision

Quick steps:
1. Find a task in [TODO.md](docs/TODO.md) or create an issue
2. Fork the repository
3. Create a feature branch (`git checkout -b feature/amazing-feature`)
4. Write tests first (TDD required)
5. Implement your feature
6. Run tests to ensure everything passes
7. Commit your changes (`git commit -m 'Add amazing feature'`)
8. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Original [substack-mcp](https://github.com/marcomoauro/substack-mcp) by Marco Moauro - the foundation for this project
- [python-substack](https://github.com/ma2za/python-substack) - unofficial Python library for Substack (not affiliated with Substack Inc.)
- [Model Context Protocol](https://modelcontextprotocol.io) specification by Anthropic
- The Substack team for creating an amazing platform (though we have no affiliation)

## 🆘 Support

- For issues: Open an issue on [GitHub](https://github.com/ty13r/substack-mcp-plus/issues)
- For questions: Start a discussion in the [Discussions](https://github.com/ty13r/substack-mcp-plus/discussions) tab