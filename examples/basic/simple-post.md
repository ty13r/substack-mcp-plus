# Basic Example: Creating a Simple Post

This example shows how to create a basic draft post using Claude Desktop.

## Setup

1. Make sure you've run `python setup_auth.py` and authenticated
2. Ensure Claude Desktop is configured with the MCP server

## Example Conversation

**You:** Create a draft post titled "My First Newsletter" with the content: "Welcome to my newsletter! This is my first post using the Substack MCP server. I'm excited to share my thoughts with you all."

**Claude will:**
1. Use the `create_formatted_post` tool
2. Create a draft with your title and content
3. Return the post ID and URL for editing

## What Happens

- A draft post is created in your Substack account
- The post is saved but not published
- You can edit it further in Substack's web interface
- Use `publish_post` with the post ID to publish when ready

## Common Variations

- Add a subtitle: "Create a draft with subtitle 'A new beginning'"
- Use Markdown: "Create a draft with this content: **Bold text** and *italic*"
- Include lists: "Add a bulleted list of my favorite topics"