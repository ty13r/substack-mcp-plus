# TODO - Current Work Items

This document tracks high-level tasks and their subtasks. Contributors can claim tasks by commenting on the linked issue or creating a PR referencing the task number.

**Status Legend**: 
- 🔴 Not Started
- 🟡 In Progress
- 🟢 Complete
- 🔵 Blocked

## Critical Bugs from v1.0.3 Testing

Based on comprehensive testing (July 8-9, 2025), these bugs need immediate attention:

### 🔴 CRITICAL - Data Loss/Safety Issues

#### 1. Images Silently Dropped in create_formatted_post 🔴
**Bug**: Images in content are dropped without error during post creation
**Impact**: Data loss - users lose images without knowing
**Fix**: Ensure images pass through to Substack API
**Tool**: #4
**Test Case**: Create post with markdown image `![alt](url)` - verify it appears

#### 2. Delete Draft Confirmation Bypass 🔴  
**Bug**: Test report claims delete executes without confirmation (needs verification)
**Impact**: Accidental permanent deletion risk
**Fix**: Verify and ensure confirmation is working
**Tool**: #12
**Test Case**: Try to delete without confirm_delete:true

### 🟠 HIGH PRIORITY - Broken Features

#### 3. Upload Image - Missing Implementation 🔴
**Bug**: 'APIWrapper' object has no attribute 'get_image'
**Impact**: Image uploads completely non-functional
**Fix**: Implement missing get_image method in api_wrapper.py
**Tool**: #7
**Error**: `AttributeError: 'APIWrapper' object has no attribute 'get_image'`

#### 4. Subscriber Count Output Loop 🔴
**Bug**: Text "📊 Subscriber Statistics" repeats ~50 times
**Impact**: Tool unusable despite working data retrieval
**Fix**: Fix output formatting in get_subscriber_count handler
**Tool**: #11
**Test Case**: Run get_subscriber_count and check output

#### 5. Update Post Content Fails 🔴
**Bug**: All content updates fail with 500 Internal Server Error
**Impact**: Cannot modify post content via API
**Fix**: Debug API communication for content updates
**Tool**: #5
**Error**: 500 Internal Server Error on content updates only

#### 6. Schedule Post 404 Errors 🟢 RESOLVED
**Bug**: Scheduling fails with 404 despite good validation
**Impact**: Cannot schedule posts for future publication
**Resolution**: Tool removed in v1.0.3 - python-substack library uses outdated endpoint
**Tool**: #8 (Removed)
**Error**: 404 with JSON parsing failures

### 🟡 MEDIUM PRIORITY - Wrong Behavior

#### 7. Preview Draft Wrong URL Type 🔴
**Bug**: Generates published URLs instead of draft preview URLs
**Impact**: Users get non-functional links
**Fix**: Generate correct draft preview URLs with draft_id parameter
**Tool**: #9
**Expected**: URL with ?draft_id=XXX parameter

#### 8. Markdown Formatting Not Rendered 🔴
**Bug**: Bold/italic shows as **text** instead of formatted
**Impact**: Posts require manual cleanup in Substack UI
**Fix**: Already tracked in existing Task #1 below
**Tool**: #4

### 🟢 LOW PRIORITY - Cleanup

#### 9. Remove Redundant Tool 🔴
**Bug**: list_drafts_for_deletion duplicates list_drafts functionality
**Impact**: Unnecessary complexity
**Fix**: Remove tool entirely from server.py
**Tool**: #13

#### 10. Published Status Inconsistency 🔴
**Bug**: API shows posts as published that UI shows as unpublished
**Impact**: Confusing status information
**Fix**: Investigate API/UI sync issues
**Tool**: #2

---

## High Priority Tasks

### 1. Fix Text Formatting Issues 🔴
**Goal**: Make bold/italic/links render properly instead of showing markdown syntax

**Subtasks**:
- [ ] Write comprehensive tests for text formatting
- [ ] Research Substack's text mark format in python-substack library
- [ ] Implement proper text node formatting with marks
- [ ] Test with real posts to verify formatting
- [ ] Update documentation with working examples

**Claimed by**: [Available]
**Related Issues**: #[TBD]
**Estimated Effort**: Medium-High

---

### 2. Implement Rate Limiting 🔴
**Goal**: Prevent API errors from too many requests

**Subtasks**:
- [ ] Research Substack's actual rate limits (undocumented)
- [ ] Design rate limiting strategy (per-endpoint limits)
- [ ] Implement rate limiter with exponential backoff
- [ ] Add configuration options for rate limits
- [ ] Write tests for rate limiting behavior
- [ ] Update documentation

**Claimed by**: [Available]
**Related Issues**: #[TBD]
**Estimated Effort**: Medium

---

### 3. Improve Test Coverage to 70% 🟡
**Goal**: Increase coverage from 51% to 70% (focus on critical paths)

**Subtasks**:
- [ ] Add tests for auth_manager.py (0% → 80%)
- [ ] Add tests for api_wrapper.py (26% → 80%)
- [ ] Add tests for tool modules (0% → 90%)
- [ ] Fix failing tests in auth_handler.py
- [ ] Add integration tests for post creation flow
- [ ] Update coverage report

**Claimed by**: [Available]
**Related Issues**: #[TBD]
**Estimated Effort**: Medium
**Progress**: See [Coverage Report](COVERAGE_REPORT.md)

---

## Medium Priority Tasks

### 4. Add Batch Operations Support 🔴
**Goal**: Process multiple posts at once

**Subtasks**:
- [ ] Design batch API interface
- [ ] Implement batch create_post
- [ ] Implement batch update_post
- [ ] Implement batch publish_post
- [ ] Add progress tracking
- [ ] Handle partial failures gracefully
- [ ] Write comprehensive tests

**Claimed by**: [Available]
**Related Issues**: #[TBD]
**Estimated Effort**: High

---

### 5. Create Template System 🔴
**Goal**: Allow users to save and reuse post templates

**Subtasks**:
- [ ] Design template format (YAML/JSON)
- [ ] Create template storage mechanism
- [ ] Implement template CRUD operations
- [ ] Add template variables/placeholders
- [ ] Create example templates
- [ ] Write tests and documentation

**Claimed by**: [Available]
**Related Issues**: #[TBD]
**Estimated Effort**: Medium

---

## Bug Fixes

### 6. Fix Blockquote Formatting 🔴
**Goal**: Blockquotes should render as styled blocks, not with > prefix

**Subtasks**:
- [ ] Research Substack's blockquote format
- [ ] Update block_builder.py for proper format
- [ ] Test with various blockquote styles
- [ ] Update examples

**Claimed by**: [Available]
**Related Issues**: #[TBD]
**Estimated Effort**: Low

---

### 7. Fix Link Display Issues 🔴
**Goal**: Links should be clickable, not show as [text](url)

**Subtasks**:
- [ ] Debug current link implementation
- [ ] Fix link mark format
- [ ] Test with various link types
- [ ] Verify in published posts

**Claimed by**: [Available]
**Related Issues**: #[TBD]
**Estimated Effort**: Low-Medium

---

## Documentation Tasks

### 8. Create Video Tutorial 🔴
**Goal**: 5-minute setup and usage video

**Subtasks**:
- [ ] Write script/outline
- [ ] Record installation process
- [ ] Record basic usage demo
- [ ] Edit and add captions
- [ ] Upload and link in README

**Claimed by**: [Available]
**Related Issues**: #[TBD]
**Estimated Effort**: Medium

---

## How to Claim a Task

1. **Check if available**: Ensure "Claimed by" shows [Available]
2. **Comment on issue**: If an issue exists, comment that you're working on it
3. **Create issue**: If no issue exists, create one referencing this TODO item
4. **Update this file**: Submit a PR updating "Claimed by" with your GitHub username
5. **Start work**: Follow our [Contributing Guide](../CONTRIBUTING.md)

## Adding New Tasks

To add a new high-level task:

1. Follow the format above
2. Include clear goal and subtasks
3. Estimate effort (Low/Medium/High)
4. Link related issues if they exist
5. Submit PR to update this file

## Completed Tasks

Once a task is fully complete:
1. Move it to a "Completed Tasks" section at the bottom
2. Include completion date and contributor
3. Link to the implementing PR(s)

---

## User Experience Enhancements

### 9. Improve update_post UX - Add Partial Edit Mode 🔴
**Goal**: Allow users to make small edits without replacing entire content

**Subtasks**:
- [ ] Design 'patch' mode API that accepts edit instructions
- [ ] Implement content diffing/merging logic
- [ ] Add support for line-based or paragraph-based edits
- [ ] Create intuitive edit syntax (e.g., "replace paragraph 3 with...")
- [ ] Add safety checks to prevent accidental overwrites
- [ ] Write comprehensive tests
- [ ] Update documentation with examples

**Claimed by**: [Available]
**Related Issues**: #[TBD]
**Estimated Effort**: Medium
**Priority**: Medium

---

### 10. Add Draft Autosave/Versioning 🔴
**Goal**: Prevent accidental content loss with automatic versioning

**Subtasks**:
- [ ] Design version storage system
- [ ] Implement automatic draft snapshots before updates
- [ ] Add version history viewing
- [ ] Create restore/rollback functionality
- [ ] Add configurable retention policy
- [ ] Write tests for version management
- [ ] Document versioning workflow

**Claimed by**: [Available]
**Related Issues**: #[TBD]
**Estimated Effort**: Medium
**Priority**: Medium

---

### 11. Add Search/Filter for Posts 🔴
**Goal**: Help users find specific drafts and published posts quickly

**Subtasks**:
- [ ] Implement search by title/content
- [ ] Add date range filtering
- [ ] Add status filtering (draft/published/scheduled)
- [ ] Add tag/section filtering
- [ ] Create sorted results with relevance
- [ ] Add pagination for large result sets
- [ ] Write tests and documentation

**Claimed by**: [Available]
**Related Issues**: #[TBD]
**Estimated Effort**: Medium
**Priority**: Medium

---

### 12. Add Image Upload from Chat/Clipboard 🔴
**Goal**: Allow direct image upload from chat without saving to disk first

**Subtasks**:
- [ ] Research MCP image data handling capabilities
- [ ] Implement base64 image data reception
- [ ] Add clipboard image support
- [ ] Create temporary file handling
- [ ] Add image format validation
- [ ] Clean up temporary files after upload
- [ ] Write tests and documentation

**Claimed by**: [Available]
**Related Issues**: #[TBD]
**Estimated Effort**: Medium
**Priority**: Medium

---

## Low Priority Tasks

### 13. Add Batch Operations Support 🔴
**Goal**: Process multiple posts at once for efficiency

**Subtasks**:
- [ ] Design batch operation API
- [ ] Implement batch publish
- [ ] Implement batch delete with safety checks
- [ ] Add progress tracking and reporting
- [ ] Handle partial failures gracefully
- [ ] Add rollback capability
- [ ] Write tests and documentation

**Claimed by**: [Available]
**Related Issues**: #[TBD]
**Estimated Effort**: Medium
**Priority**: Low

---

### 14. Add Content Templates 🔴
**Goal**: Provide reusable post templates for common formats

**Subtasks**:
- [ ] Design template format (YAML/JSON)
- [ ] Create built-in templates (newsletter, tutorial, etc.)
- [ ] Implement template storage and management
- [ ] Add template variables/placeholders
- [ ] Create template preview functionality
- [ ] Allow custom template creation
- [ ] Write tests and documentation

**Claimed by**: [Available]
**Related Issues**: #[TBD]
**Estimated Effort**: Low
**Priority**: Low

---

### 15. Enhance list_drafts with Rich Preview 🔴
**Goal**: Show more useful information in draft listings

**Subtasks**:
- [ ] Add content excerpt/preview (first 200 chars)
- [ ] Add word count and estimated reading time
- [ ] Show last modified timestamp
- [ ] Add section/category info
- [ ] Show paywall status
- [ ] Format output for better readability
- [ ] Write tests

**Claimed by**: [Available]
**Related Issues**: #[TBD]
**Estimated Effort**: Low
**Priority**: Low

---

### 16. Add Import from External Sources 🔴
**Goal**: Import content from Google Docs, Notion, etc.

**Subtasks**:
- [ ] Research external API integrations
- [ ] Implement Google Docs import
- [ ] Implement Notion import
- [ ] Implement Markdown file import
- [ ] Handle formatting conversion
- [ ] Preserve images and links
- [ ] Write tests and documentation

**Claimed by**: [Available]
**Related Issues**: #[TBD]
**Estimated Effort**: High
**Priority**: Low

---

### 17. Add Export/Backup Functionality 🔴
**Goal**: Allow users to backup their drafts locally

**Subtasks**:
- [ ] Design export format (Markdown + metadata)
- [ ] Implement single draft export
- [ ] Implement bulk export with folder structure
- [ ] Add metadata preservation (dates, settings)
- [ ] Create import functionality for backups
- [ ] Add scheduled backup option
- [ ] Write tests and documentation

**Claimed by**: [Available]
**Related Issues**: #[TBD]
**Estimated Effort**: Low
**Priority**: Low

---

### 18. Fork/Improve python-substack Library 🔴
**Goal**: Address limitations in the unmaintained python-substack library

**Context**: The python-substack library hasn't been updated in 2+ years, causing:
- Scheduling endpoints don't work (404 errors)
- Image handling issues with captioned_image()
- Subscriber count API limitations
- Outdated endpoints and missing features

**Subtasks**:
- [ ] Fork python-substack repository
- [ ] Audit current API endpoints vs Substack's actual API
- [ ] Fix scheduling endpoint (if possible)
- [ ] Fix image handling methods
- [ ] Add proper error handling for all API responses
- [ ] Update documentation
- [ ] Consider maintaining as community fork
- [ ] Publish updated package

**Claimed by**: [Available]
**Related Issues**: #[TBD]
**Estimated Effort**: High
**Note**: This is a significant undertaking that would benefit the entire Substack developer community

---

*Last updated: July 2025*