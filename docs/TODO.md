# TODO - Current Work Items

This document tracks high-level tasks and their subtasks. Contributors can claim tasks by commenting on the linked issue or creating a PR referencing the task number.

**Status Legend**: 
- 🔴 Not Started
- 🟡 In Progress
- 🟢 Complete
- 🔵 Blocked

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

*Last updated: January 2025*