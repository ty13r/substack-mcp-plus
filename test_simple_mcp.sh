#!/bin/bash
# Simple test of MCP server with initialization

export SUBSTACK_PUBLICATION_URL="https://neroaugustus.substack.com/"

# Test with proper MCP initialization sequence
echo '{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"0.1.0","capabilities":{},"clientInfo":{"name":"test","version":"1.0.0"}},"id":1}
{"jsonrpc":"2.0","method":"initialized","params":{}}
{"jsonrpc":"2.0","method":"tools/call","params":{"name":"list_drafts","arguments":{"limit":5}},"id":2}' | /opt/homebrew/bin/substack-mcp-plus