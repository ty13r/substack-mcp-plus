# Substack MCP Plus Troubleshooting Guide

## Common Issues and Solutions

### 1. "Post not found" Errors

**Symptoms:**
- get_post_content returns "Post not found"
- duplicate_post returns "Post not found"

**Possible Causes:**
- Invalid post ID
- Post belongs to a different publication
- Authentication issues
- Post was deleted

**Solutions:**
1. Verify the post ID using `list_drafts` or `list_published`
2. Ensure you're authenticated to the correct publication
3. Check if the post still exists in Substack

### 2. "Unable to get subscriber count" Error

**Symptoms:**
- get_subscriber_count fails with "Unable to get subscriber count from publication or sections"

**Possible Causes:**
- API endpoint changes
- Insufficient permissions
- Publication settings blocking subscriber count access
- Authentication token lacks required scopes

**Solutions:**
1. Verify your authentication has admin/owner privileges
2. Check if subscriber count is visible in Substack dashboard
3. Try re-authenticating with `python setup_auth.py`

### 3. Authentication Issues

**Symptoms:**
- "Authentication failed" errors
- Tools work initially but fail later
- Session token expiration

**Solutions:**
1. Re-run authentication setup:
   ```bash
   python setup_auth.py
   ```
2. Clear cached credentials:
   ```bash
   rm -rf ~/.substack_mcp/
   ```
3. Use email/password authentication if session tokens fail

### 4. Body Content Formatting Issues

**Symptoms:**
- Posts appear but content is missing
- "Post body is not a dict" warnings in logs

**Possible Causes:**
- Legacy posts with different format
- API returning unexpected data structure
- Posts created outside of this tool

**Solutions:**
- These posts can still be listed and managed, but content extraction may be limited
- Use Substack's web interface for these posts

## Debugging Steps

### 1. Enable Debug Logging

Set the environment variable:
```bash
export SUBSTACK_MCP_DEBUG=true
```

### 2. Test Authentication

```python
# Test if you can list drafts
list_drafts

# Test if you can get your publication info
get_sections
```

### 3. Verify Post IDs

Always verify post IDs before operations:
```python
# List all drafts with their IDs
list_drafts limit=20

# Use the exact ID shown
get_post_content post_id="exact-id-from-list"
```

### 4. Check API Response

If you see "API returned invalid data format", it usually means:
- The API response structure has changed
- The post data is in an unexpected format
- Authentication is partially failing

## Known Limitations

1. **Subscriber Count**: May not be available for all account types
2. **Legacy Posts**: Older posts may have different data structures
3. **Formatting**: Bold/italic in-text formatting has limited support
4. **API Changes**: Substack's private API may change without notice

## Getting Help

1. Check the logs for detailed error messages
2. Ensure you're using the latest version
3. Report issues at: https://github.com/baba786/substack-mcp-client/issues
4. Include:
   - Error messages
   - Steps to reproduce
   - Your publication URL (without credentials)

## Quick Fixes

### "It was working yesterday"
→ Re-authenticate: `python setup_auth.py`

### "Can't find my post"
→ Use `list_drafts` to see all available posts with IDs

### "Everything is broken"
→ Clear cache and re-authenticate:
```bash
rm -rf ~/.substack_mcp/
python setup_auth.py
```