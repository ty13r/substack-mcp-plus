# Confirmation System Documentation

## Overview

To prevent accidental data loss or unwanted actions, we've implemented a comprehensive confirmation system across all MCP tools that modify data. This ensures that LLMs cannot accidentally overwrite user content or perform irreversible actions without explicit user consent.

## How It Works

### Simple Yes/No Confirmation

When an LLM attempts to perform a risky action without confirmation, they receive a warning message:

```
⚠️ CONFIRMATION REQUIRED ⚠️

You are about to UPDATE this draft:
- Post: "My Important Article"
- Changes:
  - Subtitle: "New subtitle"

⚡ This will OVERWRITE any manual edits you've made to these fields.

Are you sure you want to update this draft?

To confirm, simply say "yes" or tell me to proceed.
To cancel, say "no" or tell me to stop.
```

Users can simply respond with:
- "Yes" / "Proceed" / "Go ahead" → LLM will re-call the tool with confirmation
- "No" / "Stop" / "Cancel" → LLM will cancel the operation

### Protected Tools

The following tools require explicit confirmation:

1. **update_post** (HIGH RISK)
   - Parameter: `confirm_update: true`
   - Risk: Can overwrite existing content

2. **publish_post** (HIGH RISK)
   - Parameter: `confirm_publish: true`
   - Risk: Irreversible, sends emails to subscribers

3. **schedule_post** (HIGH RISK)
   - Parameter: `confirm_schedule: true`
   - Risk: Will auto-publish at scheduled time

4. **create_formatted_post** (MEDIUM RISK)
   - Parameter: `confirm_create: true`
   - Risk: Creates new drafts that could clutter account

5. **duplicate_post** (MEDIUM RISK)
   - Parameter: `confirm_duplicate: true`
   - Risk: Creates copies that could clutter account

6. **delete_draft** (HIGH RISK)
   - Parameter: `confirm_delete: true`
   - Risk: Permanently deletes content
   - Note: This already had confirmation before our update

### Implementation Details

Each protected tool follows this pattern:

```python
if not arguments.get("confirm_update", False):
    # Show warning with details about what will happen
    return warning_message
else:
    # Proceed with the action
    return perform_action()
```

### Tool Descriptions

All tool descriptions have been updated to guide LLM behavior:

```
"IMPORTANT: Always ask for user confirmation before updating. 
When user confirms with 'yes' or similar, call this tool again 
with confirm_update: true."
```

## Benefits

1. **Prevents Accidents**: LLMs cannot accidentally modify or destroy user content
2. **User Control**: Clear opportunity to stop unwanted actions
3. **Transparency**: Shows exactly what will happen before it happens
4. **Simple UX**: Just say "yes" or "no" - no complex parameters to remember
5. **Consistency**: Same pattern across all risky tools

## Testing

Comprehensive tests ensure the confirmation system works correctly:
- `tests/test_confirmation_simple.py` - 7 tests covering all confirmation logic

## Partial Updates

The `update_post` tool supports partial updates - you can update individual fields without affecting others:

- Update only subtitle: `update_post(post_id="xxx", subtitle="New subtitle")`
- Update only title: `update_post(post_id="xxx", title="New title")`
- Update multiple: `update_post(post_id="xxx", title="New", subtitle="Also new")`

**Important**: Only the fields you specify will be updated. Other fields remain untouched.

## Example Interaction

```
User: "I like this subtitle better: 'New and Improved'"
LLM: "I'll update the subtitle for you."
[Calls update_post without confirmation]

System: ⚠️ CONFIRMATION REQUIRED ⚠️
You are about to UPDATE this draft:
- Post: "My Blog Post"
- Changes:
  - Subtitle: "New and Improved"

⚡ This will ONLY update the fields listed above.
⚡ Other fields (like content) will remain unchanged.

Are you sure you want to update this draft?

User: "Yes"
LLM: [Calls update_post with confirm_update: true]
System: ✅ Post updated successfully!
```

This system ensures that users always have control over their content and prevents the frustrating experience of accidental overwrites or deletions.