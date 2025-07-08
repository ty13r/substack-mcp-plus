# Substack MCP Plus Examples

This directory contains examples demonstrating how to use the Substack MCP Plus server.

## 📁 Directory Structure

- **[basic/](basic/)** - Simple examples for getting started
  - `simple-post.md` - Creating a basic draft post
  
- **[advanced/](advanced/)** - Complex formatting and features
  - `formatted-post-with-images.md` - Rich text, images, and scheduling
  
- **[cli/](cli/)** - Command line and programmatic usage
  - `direct-usage.md` - Using the MCP server directly

## 🚀 Getting Started

1. **First Time Setup**:
   ```bash
   # Install the package
   npm install -g substack-mcp-plus
   
   # Run authentication setup
   substack-mcp-plus-setup
   ```

2. **Configure Claude Desktop** - See [cli/direct-usage.md](cli/direct-usage.md)

3. **Try Basic Example** - Start with [basic/simple-post.md](basic/simple-post.md)

## 📝 Example Categories

### Basic Usage
Perfect for first-time users:
- Creating simple drafts
- Basic text formatting
- Publishing posts

### Advanced Features
For power users:
- Rich text formatting (headers, lists, code blocks)
- Image uploads and embedding
- Post scheduling
- Bulk operations

### Developer Integration
For building on top of the MCP server:
- Direct CLI usage
- SDK integration
- Custom client examples

## 💡 Tips

1. **Always authenticate first** - Run `setup_auth.py` before using any tools
2. **Test with drafts** - Create drafts before publishing to production
3. **Check formatting** - Use `get_post_content` to verify formatting
4. **Use the right tool** - Each tool has a specific purpose (see main README)

## 🔗 More Resources

- [Full Documentation](../docs/)
- [API Reference](../README.md#-available-tools)
- [Troubleshooting Guide](../docs/TROUBLESHOOTING.md)
- [Known Issues](../docs/KNOWN_ISSUES.md)