# Complete Claude Desktop Testing Guide for Substack MCP Plus

## Pre-Test Setup

### 1. Start Fresh
```bash
# Kill any existing MCP processes
pkill -f substack-mcp-plus

# Clear any test drafts from your Substack account (optional)
# Log into Substack web UI and delete test drafts
```

### 2. Verify Installation
```bash
# Check the server is installed
which substack-mcp-plus

# Verify authentication is set up
cd $(npm root -g)/substack-mcp-plus
cat .env  # Should show your encrypted tokens
```

### 3. Restart Claude Desktop
- Quit Claude Desktop completely (Cmd+Q on Mac)
- Reopen Claude Desktop
- You should see "substack-mcp-plus" in the tools menu (🔨 icon)

## Testing All 14 Tools

### Tool 1: create_formatted_post ✅
**Test the confirmation system and rich formatting**

```
Test 1A - Basic Creation with Confirmation:
1. Say: "Create a new Substack draft with the title 'Test Post 1' and content 'This is a test'"
2. EXPECT: Confirmation warning appears
3. Say: "No" 
4. VERIFY: Draft is NOT created
5. Repeat step 1, then say "Yes"
6. VERIFY: Draft is created successfully

Test 1B - Rich Formatting:
Say: "Create a draft titled 'Formatting Test' with this content:
# Main Header
This has **bold** and *italic* text.
- Bullet point 1
- Bullet point 2

```python
def hello():
    print('Code block test')
```

> This is a blockquote

Free content here.

<!--paywall-->

Premium content here."

7. EXPECT: Confirmation prompt
8. Say: "Yes"
9. VERIFY: Draft created with ID
10. Check on Substack.com that formatting is preserved
```

### Tool 2: list_drafts ✅
**No confirmation needed - read-only operation**

```
Test 2A - List Recent Drafts:
1. Say: "Show me my recent Substack drafts"
2. VERIFY: List shows your test drafts with IDs and titles
3. Note down a draft ID for next tests (e.g., "draft-123")

Test 2B - List with Limit:
1. Say: "Show me my last 5 drafts"
2. VERIFY: Maximum 5 drafts shown
```

### Tool 3: update_post ✅
**Test partial updates and confirmation**

```
Test 3A - Update Subtitle Only:
1. Say: "Update draft [ID] with subtitle 'New Subtitle Test'"
2. EXPECT: Confirmation warning showing:
   - Post title
   - Changes: subtitle only
   - "This will ONLY update the fields listed above"
3. Say: "No"
4. VERIFY: No changes made

Test 3B - Confirm Update:
1. Repeat Test 3A but say "Yes" 
2. VERIFY: Success message
3. Check Substack.com - only subtitle changed, content intact

Test 3C - Update Title Only:
1. Say: "Change the title of draft [ID] to 'Updated Title'"
2. EXPECT: Confirmation showing title change only
3. Say: "Yes"
4. VERIFY: Only title updated

Test 3D - Update Multiple Fields:
1. Say: "Update draft [ID] with title 'Multi Update' and subtitle 'Also Updated'"
2. EXPECT: Confirmation showing both changes
3. Say: "Yes"
4. VERIFY: Both fields updated
```

### Tool 4: get_post_content ✅
**Read-only operation - no confirmation needed**

```
Test 4A - Read Draft Content:
1. Say: "Show me the full content of draft [ID]"
2. VERIFY: Shows:
   - Title
   - Subtitle
   - Full content with formatting
   - Status (draft/published)
```

### Tool 5: duplicate_post ✅
**Test duplication with confirmation**

```
Test 5A - Duplicate with Default Title:
1. Say: "Duplicate draft [ID]"
2. EXPECT: Confirmation showing:
   - Original title
   - New title will be "Copy of [original]"
3. Say: "Yes"
4. VERIFY: New draft created with "Copy of" prefix

Test 5B - Duplicate with Custom Title:
1. Say: "Duplicate draft [ID] with title 'Custom Copy Title'"
2. EXPECT: Confirmation with custom title
3. Say: "Yes"
4. VERIFY: New draft with custom title
```

### Tool 6: preview_draft ✅
**Read-only - generates preview link**

```
Test 6A - Generate Preview:
1. Say: "Generate a preview link for draft [ID]"
2. VERIFY: Returns preview URL
3. Open URL in browser - should show draft preview
```

### Tool 7: schedule_post ⚠️
**Test scheduling with confirmation**

```
Test 7A - Schedule for Future:
1. Say: "Schedule draft [ID] for tomorrow at 10am"
2. EXPECT: Confirmation showing:
   - Post title
   - Formatted date/time
   - Warning about auto-publish
3. Say: "No" 
4. VERIFY: Not scheduled

Test 7B - Actually Schedule (CAREFUL!):
1. Create a test draft first
2. Say: "Schedule draft [NEW_ID] for [future date]"
3. Say: "Yes"
4. VERIFY: Shows scheduled successfully
5. CHECK Substack.com - post should show as scheduled
```

### Tool 8: publish_post ⚠️
**DANGER: This sends emails! Use test account if possible**

```
Test 8A - Publish Confirmation:
1. Create a test draft titled "DELETE ME - TEST POST"
2. Say: "Publish draft [TEST_ID]"
3. EXPECT: Confirmation showing:
   - Post title
   - Subscriber count
   - "This CANNOT be undone"
4. Say: "No"
5. VERIFY: Still a draft

Test 8B - Actually Publish (VERY CAREFUL!):
Only if using test account:
1. Say "Yes" to publish
2. VERIFY: Published successfully
3. Delete from Substack.com immediately
```

### Tool 9: upload_image ✅
**No confirmation needed**

```
Test 9A - Upload Local Image:
1. Save a test image to your desktop
2. Say: "Upload image /Users/[yourname]/Desktop/test.jpg"
3. VERIFY: Returns Substack CDN URL
4. Open URL - should show your image
```

### Tool 10: delete_draft ✅
**Already has confirmation**

```
Test 10A - Delete with Confirmation:
1. Say: "Delete draft [ID]"
2. EXPECT: Confirmation warning
3. Say: "Delete draft [ID] and confirm with true"
4. VERIFY: Draft deleted
```

### Tool 11: list_drafts_for_deletion ✅
**Read-only - lists drafts with deletion instructions**

```
Test 11A - List for Deletion:
1. Say: "Show drafts for deletion"
2. VERIFY: Shows drafts with:
   - IDs
   - Titles  
   - Last updated dates
   - Example delete command
```

### Tool 12: list_published ✅
**Read-only operation**

```
Test 12A - List Published Posts:
1. Say: "Show my published posts"
2. VERIFY: Shows published posts with dates
```

### Tool 13: get_sections ✅
**Read-only operation**

```
Test 13A - Get Publication Sections:
1. Say: "Show my Substack sections"
2. VERIFY: Lists sections/categories if any
```

### Tool 14: get_subscriber_count ✅
**Read-only operation**

```
Test 14A - Get Subscribers:
1. Say: "How many subscribers do I have?"
2. VERIFY: Shows subscriber count
```

## Edge Cases to Test

### Test Formatting Edge Cases
```
1. Create a post with complex formatting:
   - Nested lists
   - Multiple code blocks
   - Links: [Test](https://example.com)
   - Images: ![Alt](https://example.com/image.jpg)
   
2. Test paywall marker variations:
   - <!--paywall-->
   - <!-- paywall -->
   - <!--PAYWALL-->
```

### Test Error Handling
```
1. Try to update non-existent post:
   Say: "Update draft invalid-id-12345"
   EXPECT: Error message

2. Try to upload non-existent image:
   Say: "Upload image /fake/path/image.jpg"
   EXPECT: Error message

3. Try invalid scheduling:
   Say: "Schedule draft [ID] for yesterday"
   EXPECT: Error about past date
```

### Test Confirmation Cancellations
```
For each tool with confirmation:
1. Trigger the confirmation
2. Say various forms of "no":
   - "No"
   - "Cancel"  
   - "Stop"
   - "Don't do it"
3. VERIFY: Action cancelled
```

## Final Verification Checklist

- [ ] All 14 tools appear in Claude Desktop
- [ ] Confirmation prompts work for all 5 protected tools
- [ ] Saying "no" cancels operations
- [ ] Saying "yes" proceeds with operations
- [ ] Partial updates only change specified fields
- [ ] Rich text formatting is preserved
- [ ] Paywall markers work correctly
- [ ] Error messages are helpful
- [ ] Preview links are functional
- [ ] Image uploads return valid URLs
- [ ] No tools execute without appropriate confirmation

## Publishing Preparation

Once all tests pass:

1. **Clean up test posts** from your Substack account
2. **Document any issues** found during testing
3. **Update CHANGELOG.md** with test results
4. **Verify package.json** version number
5. **Run final test suite**: 
   ```bash
   cd /path/to/substack-mcp-plus
   npm test
   ```

## Notes

- Test with a real Substack account but be VERY careful with publish_post
- Consider using a test publication if you have one
- The confirmation system should prevent accidents, but stay alert
- If any test fails, note the exact error message for debugging

Remember: The goal is to ensure a smooth experience for users who will rely on this tool for their publishing workflow!