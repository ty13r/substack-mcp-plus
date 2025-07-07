# Substack MCP Plus - Quick Start Guide

Get up and running with Substack MCP Plus in under 2 minutes!

## 🚀 Quick Setup

```bash
# Install globally via NPM
npm install -g substack-mcp-plus

# Run the authentication setup wizard  
python setup_auth.py
```

**That's it!** The setup wizard handles everything:
- ✅ Choice of magic link or password authentication
- ✅ Browser-based login
- ✅ CAPTCHA handling
- ✅ Secure token storage
- ✅ Automatic configuration

## 🔧 Claude Desktop Config

After running setup, add this minimal config to Claude Desktop:

```json
{
  "mcpServers": {
    "substack-mcp-plus": {
      "command": "substack-mcp-plus",
      "env": {
        "SUBSTACK_PUBLICATION_URL": "https://YOUR-PUBLICATION.substack.com"
      }
    }
  }
}
```

**Important**: Replace `YOUR-PUBLICATION` with your actual Substack subdomain (e.g., if your Substack is at `https://johndoe.substack.com`, use `johndoe`).

If you already have other MCP servers configured, add this alongside them:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/directory"]
    },
    "substack-mcp-plus": {
      "command": "substack-mcp-plus",
      "env": {
        "SUBSTACK_PUBLICATION_URL": "https://YOUR-PUBLICATION.substack.com"
      }
    }
  }
}
```

**No passwords or tokens needed!** Authentication is handled automatically.

**Config file locations:**
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

## 🧪 Test Your Setup

In Claude Desktop, try these commands:

```
# List your drafts
Show me my draft posts

# Create a simple post
Create a draft titled "Hello World" with content "This is my first post!"

# Create a formatted post
Create a draft with title "Formatted Post" and content:
# Main Header
This has **bold** and *italic* text.
- Bullet point 1
- Bullet point 2

> A blockquote for emphasis

# Upload an image
Upload image from https://picsum.photos/800/400 optimized for web
```

## 📊 Available Tools

1. **create_formatted_post** - Create posts with rich formatting
2. **update_post** - Update existing drafts
3. **publish_post** - Publish or schedule posts
4. **list_drafts** - List your draft posts
5. **upload_image** - Upload images to Substack CDN

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "No authentication found" | Run `python setup_auth.py` |
| CAPTCHA appears | Solve it in the browser window |
| Token expired | Run `python setup_auth.py` again |
| Import errors | Make sure you ran `pip install -e .` |

## 🎯 Pro Tips

1. **Markdown Support**: Full CommonMark + tables, code blocks, etc.
2. **Paywall Marker**: Use `<!-- PAYWALL -->` in your content
3. **Batch Operations**: Ask Claude to create multiple posts at once
4. **Image Optimization**: Use the upload_image tool for best performance

## 🔑 Alternative Setup (Advanced)

If you prefer manual setup or need CI/CD configuration:

### Environment Variables
```bash
export SUBSTACK_EMAIL="your-email@example.com"
export SUBSTACK_PASSWORD="your-password"
export SUBSTACK_PUBLICATION_URL="https://yourpub.substack.com"
```

### Session Token (If you have one)
```bash
export SUBSTACK_SESSION_TOKEN="s%3AYourToken..."
export SUBSTACK_PUBLICATION_URL="https://yourpub.substack.com"
```

## 📚 More Resources

- [Full Documentation](docs/)
- [Authentication Guide](docs/authentication.md)
- [Formatting Examples](docs/formatting.md)
- [Testing Guide](docs/testing_guide.md)

---

**Need help?** The authentication system provides clear error messages and guidance. For most issues, running `python setup_auth.py` will solve the problem!