# Claude Desktop Test Checklist for Substack MCP Plus

## Quick Test Order (Safest First)

### 🟢 Safe Tools (Read-Only) - Test These First
1. `list_drafts` - Shows your drafts
2. `get_post_content` - Reads a draft
3. `list_published` - Shows published posts  
4. `get_sections` - Shows publication sections
5. `get_subscriber_count` - Shows subscriber count
6. `preview_draft` - Generates preview link
7. `list_drafts_for_deletion` - Shows drafts with delete instructions

### 🟡 Medium Risk Tools (Create Content)
8. `create_formatted_post` - Creates new drafts (with confirmation)
9. `duplicate_post` - Copies existing posts (with confirmation)
10. `upload_image` - Uploads images to CDN

### 🔴 High Risk Tools (Modify/Delete Content)
11. `update_post` - Updates existing drafts (with confirmation)
12. `delete_draft` - Deletes drafts (with confirmation)
13. `schedule_post` - Schedules for auto-publish (with confirmation)
14. `publish_post` - PUBLISHES AND SENDS EMAILS (with confirmation)

## Essential Test Scenarios

### 1. Test the Confirmation System
```
Say: "Create a draft titled 'Test' with content 'test'"
EXPECT: ⚠️ CONFIRMATION REQUIRED ⚠️
Say: "no"
VERIFY: Nothing created

Say: "Create a draft titled 'Test' with content 'test'"  
Say: "yes"
VERIFY: Draft created
```

### 2. Test Partial Updates
```
Say: "Update draft [ID] subtitle to 'New Subtitle Only'"
EXPECT: Shows ONLY subtitle will change
Say: "yes"
VERIFY: Only subtitle changed on Substack.com
```

### 3. Test Rich Formatting
```
Create a draft with:
# Header
**Bold** and *italic*
- List items
```code block```
> Quote
<!--paywall-->
Premium content

VERIFY: All formatting appears correctly on Substack
```

### 4. Test Safety Features
```
For each risky tool:
1. Try the action
2. Get confirmation prompt
3. Say "no" or "cancel"
4. Verify nothing happened
```

## Pre-Flight Checklist

- [ ] Claude Desktop restarted
- [ ] MCP server shows in tools menu
- [ ] Have a test draft ID ready
- [ ] Have a test image file ready
- [ ] Know your publication URL

## Post-Test Cleanup

- [ ] Delete all test drafts
- [ ] Check no accidental publishes
- [ ] Document any issues found
- [ ] Clean up uploaded test images

## Red Flags (Stop Testing If These Occur)

- ❌ Any tool executes without confirmation when it should ask
- ❌ Update_post changes more than specified fields  
- ❌ Publish_post doesn't show clear warnings
- ❌ Errors that expose credentials
- ❌ Server crashes or hangs

## Success Criteria

✅ All 14 tools accessible in Claude Desktop
✅ All confirmations work (can cancel with "no")
✅ Partial updates only change specified fields
✅ Rich text formatting preserved
✅ No data loss or unexpected changes
✅ Clear error messages for invalid operations

---

⚠️ **REMEMBER**: publish_post sends emails to ALL subscribers. Only test on a test account or be VERY careful!