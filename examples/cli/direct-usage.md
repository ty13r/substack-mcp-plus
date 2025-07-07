# CLI Example: Direct MCP Server Usage

This example shows how to interact with the MCP server directly from the command line.

## Testing the Server

```bash
# Start the server
substack-mcp-plus

# In another terminal, send a test request
echo '{"jsonrpc": "2.0", "method": "tools/list", "params": {}, "id": 1}' | substack-mcp-plus
```

## Claude Desktop Configuration

Add to your Claude Desktop config file:

### macOS
`~/Library/Application Support/Claude/claude_desktop_config.json`

### Windows
`%APPDATA%\Claude\claude_desktop_config.json`

### Linux
`~/.config/claude/claude_desktop_config.json`

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

## Using with Other MCP Clients

```javascript
// Example using MCP SDK
import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';

const transport = new StdioClientTransport({
  command: 'substack-mcp-plus'
});

const client = new Client({
  name: 'example-client',
  version: '1.0.0'
}, {
  capabilities: {}
});

await client.connect(transport);

// List available tools
const tools = await client.listTools();
console.log('Available tools:', tools);

// Create a post
const result = await client.callTool({
  name: 'create_formatted_post',
  arguments: {
    title: 'Test Post',
    content: 'This is a test post from the MCP client',
    content_type: 'markdown'
  }
});
```

## Debugging

```bash
# Enable debug logging
export DEBUG=mcp:*
substack-mcp-plus

# Check server info
echo '{"jsonrpc": "2.0", "method": "initialize", "params": {"capabilities": {}}, "id": 1}' | substack-mcp-plus
```

## Common Issues

1. **"Python not found"**: Make sure Python 3.10+ is installed
2. **"Module not found"**: Run `pip install -e .` in the project directory
3. **"Authentication failed"**: Run `python setup_auth.py` to re-authenticate