# Test Installation Instructions

## Method 1: Global Install from Tarball (Recommended)

```bash
# 1. First uninstall any existing version
npm uninstall -g substack-mcp-plus

# 2. Install from the tarball
npm install -g ./substack-mcp-plus-1.0.3.tgz

# 3. Verify installation
which substack-mcp-plus
# Should show: /opt/homebrew/bin/substack-mcp-plus

# 4. Test the command works
substack-mcp-plus-setup --help
```

## Method 2: Test in Isolated Directory

```bash
# 1. Create a test directory
mkdir -p ~/test-substack-mcp
cd ~/test-substack-mcp

# 2. Install the package locally
npm install ../myApps/substack-mcp-plus/substack-mcp-plus-1.0.3.tgz

# 3. Run from node_modules
./node_modules/.bin/substack-mcp-plus

# 4. Or configure Claude Desktop to use this path:
# "command": "/Users/Matt/test-substack-mcp/node_modules/.bin/substack-mcp-plus"
```

## Method 3: Direct Test Without NPM

```bash
# From the project directory, you can test directly:
cd /Users/Matt/myApps/substack-mcp-plus

# Run the server directly
node src/index.js

# Or with Python directly
source venv/bin/activate
python -m src.server
```

## After Testing

To revert to the published version:
```bash
# Uninstall test version
npm uninstall -g substack-mcp-plus

# Install from NPM
npm install -g substack-mcp-plus@1.0.2
```

## Notes

- The tarball includes all necessary files including the virtual environment
- The postinstall script will run automatically during installation
- Make sure to restart Claude Desktop after changing the installation