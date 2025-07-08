# Claude Desktop MCP Test Checklist for Substack MCP Plus v1.0.3

## Pre-Test Setup

1. **Clean Installation**
   ```bash
   # Uninstall current version
   npm uninstall -g substack-mcp-plus
   
   # Clear npm cache
   npm cache clean --force
   
   # Install fresh from local directory
   npm install -g .
   ```

2. **Verify Installation**
   ```bash
   which substack-mcp-plus
   # Should show: /opt/homebrew/bin/substack-mcp-plus
   ```

3. **Configure Claude Desktop**
   - Remove existing substack-mcp-plus entry from Claude Desktop config
   - Re-add with fresh configuration:
   ```json
   {
     "mcpServers": {
       "substack-mcp-plus": {
         "command": "/opt/homebrew/bin/substack-mcp-plus",
         "env": {
           "SUBSTACK_PUBLICATION_URL": "https://neroaugustus.substack.com/"
         }
       }
     }
   }
   ```
   - Restart Claude Desktop completely (Quit and reopen)

4. **Authentication Setup**
   ```bash
   # Run setup command
   substack-mcp-plus-setup
   
   # Should open browser for authentication
   # Complete login process
   # Verify success message
   ```

## Tool Testing Checklist

### 1. list_drafts ✓
**Test**: "Can you list my drafts?"
- [ ] Should return 5 drafts with titles and IDs
- [ ] No errors or "Found 0 drafts"
- [ ] IDs should be numeric

### 2. list_published
**Test**: "Show me my published posts"
- [ ] Should return published posts (if any)
- [ ] Should show publication dates
- [ ] Should have different IDs than drafts

### 3. get_post_content
**Test**: "Read the content of draft ID: 167737151" (use actual ID from list_drafts)
- [ ] Should show full formatted content
- [ ] Should preserve markdown formatting
- [ ] Should show title and subtitle

### 4. create_formatted_post
**Test 1**: "Create a draft post titled 'Test Post from Claude Desktop' with content 'This is a test post with **bold** and *italic* text.'"
- [ ] Should ask for confirmation first
- [ ] After confirming, should create draft
- [ ] Should return new post ID

**Test 2**: "Create a draft with markdown formatting:
```
Title: Markdown Test Post
Content:
# This is a heading
This is a paragraph with **bold** and *italic* text.

## Subheading
- Bullet point 1
- Bullet point 2

1. Numbered item 1
2. Numbered item 2

> This is a blockquote

\`\`\`python
def hello():
    print("Hello World")
\`\`\`
```"
- [ ] Should preserve all formatting
- [ ] Code blocks should work
- [ ] Lists should format correctly

### 5. update_post
**Test**: "Update the test post we just created. Change the title to 'Updated Test Post'"
- [ ] Should ask for confirmation
- [ ] Should successfully update
- [ ] Verify with list_drafts that title changed

### 6. duplicate_post
**Test**: "Duplicate the post with ID [use one from list_drafts]"
- [ ] Should ask for confirmation
- [ ] Should create new draft with "Copy of" prefix
- [ ] Content should be identical

### 7. upload_image
**Test**: "Upload this image: /Users/Matt/Desktop/test-image.png" (use any local image)
- [ ] Should upload successfully
- [ ] Should return Substack CDN URL
- [ ] URL should start with https://substackcdn.com/

### 8. schedule_post
**Test**: "Schedule the test post to publish tomorrow at 10 AM"
- [ ] Should ask for confirmation
- [ ] Should accept the scheduling
- [ ] Should show scheduled time

### 9. preview_draft
**Test**: "Generate a preview link for draft ID [use test post ID]"
- [ ] Should return preview URL
- [ ] URL should be clickable
- [ ] Should include draft_id parameter

### 10. get_sections
**Test**: "What sections are available in my publication?"
- [ ] Should list any sections/categories
- [ ] Should show section IDs

### 11. get_subscriber_count
**Test**: "How many subscribers do I have?"
- [ ] Should return subscriber count
- [ ] Should show publication URL

### 12. delete_draft
**Test**: "Delete the test post we created" (use the test post ID)
- [ ] Should ask for confirmation with warning
- [ ] After confirming, should delete
- [ ] Verify with list_drafts it's gone

### 13. list_drafts_for_deletion
**Test**: "Show me all drafts with delete commands"
- [ ] Should list all drafts with formatted delete commands
- [ ] Should include last updated dates
- [ ] Commands should have proper IDs

### 14. publish_post
**Test**: Only if you have a test draft ready
"Publish draft ID [use a test draft]"
- [ ] Should ask for confirmation with strong warning
- [ ] Should explain email will be sent
- [ ] (Only confirm if using test publication)

## Error Handling Tests

### Test Authentication Errors
1. **Test**: Temporarily rename ~/.substack-mcp-plus/auth.json
   ```bash
   mv ~/.substack-mcp-plus/auth.json ~/.substack-mcp-plus/auth.json.bak
   ```
2. Try "list drafts" - should show authentication error
3. Restore file:
   ```bash
   mv ~/.substack-mcp-plus/auth.json.bak ~/.substack-mcp-plus/auth.json
   ```

### Test Invalid Post IDs
**Test**: "Read post ID 99999999999"
- [ ] Should show clear error message
- [ ] Should not crash

### Test Network Issues
**Test**: Turn off WiFi and try "list drafts"
- [ ] Should show network error
- [ ] Should not hang indefinitely

## Performance Tests

### Response Times
- [ ] list_drafts should respond in < 3 seconds
- [ ] get_post_content should respond in < 3 seconds
- [ ] No operations should hang or timeout

### Multiple Operations
**Test**: Run several commands in sequence:
1. List drafts
2. Read a post
3. List published
4. Get subscriber count
- [ ] All should work without needing restart
- [ ] No memory/connection issues

## Edge Cases

### Special Characters
**Test**: "Create a draft with title 'Test: Special "Characters" & Symbols! 🎉'"
- [ ] Should handle quotes and special chars
- [ ] Should preserve emoji

### Empty Content
**Test**: "Create a draft titled 'Empty Test' with no content"
- [ ] Should show appropriate error

### Large Content
**Test**: Create a draft with very long content (paste a long article)
- [ ] Should handle without truncation
- [ ] Should complete successfully

## Final Verification

1. **Check Logs**
   ```bash
   tail -100 ~/Library/Logs/Claude/mcp-server-substack-mcp-plus.log
   ```
   - [ ] No Python tracebacks
   - [ ] No "ERROR" level messages (except for tested errors)

2. **Clean Test Data**
   - [ ] Delete all test posts created during testing
   - [ ] Verify original drafts remain intact

## Sign-off

- [ ] All core features working
- [ ] Error handling appropriate
- [ ] Performance acceptable
- [ ] No crashes or hangs
- [ ] Ready for v1.0.3 release

**Tested by**: ________________  
**Date**: ________________  
**Claude Desktop Version**: ________________