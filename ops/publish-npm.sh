#!/bin/bash
set -e

# Validate environment variables
if [ -z "$NPM_TOKEN" ]; then
  echo "Error: NPM_TOKEN is not set"
  echo "Please run: export NPM_TOKEN=your_npm_token"
  exit 1
fi

# Check if logged in to npm
if ! npm whoami &> /dev/null; then
  echo "Logging in to npm..."
  # Create .npmrc file with auth token
  echo "//registry.npmjs.org/:_authToken=$NPM_TOKEN" > ~/.npmrc
fi

# Run tests before publishing
echo "Running tests..."
cd "$(dirname "$0")/.."
if [ -d "venv" ]; then
  ./venv/bin/python -m pytest tests/test_new_tools.py tests/test_post_handler_validation.py tests/test_simple_auth_manager.py -q
fi

# Publish to npm
echo "Publishing to npm..."
npm publish --access public

echo "✅ Package published successfully to npm!"
echo "📦 View at: https://www.npmjs.com/package/substack-mcp-plus"