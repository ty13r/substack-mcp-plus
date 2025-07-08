# Known Issues and Limitations

## Current Known Issues

### 1. Text Formatting Display
- **Issue**: Bold and italic text displays as markdown syntax (`**bold**`, `*italic*`) instead of formatted text
- **Impact**: Posts show formatting markers rather than styled text
- **Workaround**: After publishing, manually edit in Substack's web editor if formatted text is required
- **Status**: Under investigation - appears to be related to how Substack's undocumented API handles text marks

### 2. Link Formatting
- **Issue**: Links display as markdown syntax (`[text](url)`) instead of clickable links
- **Impact**: Links are not clickable in the published post
- **Workaround**: Use Substack's web editor to convert to proper links after publishing
- **Status**: Known limitation of current implementation

### 3. Image Rendering
- **Issue**: Images display as markdown syntax (`![alt](url)`) instead of rendered images
- **Impact**: Images show as text rather than actual images in the editor
- **Note**: This was working in an earlier version but broke due to python-substack library issues
- **Workaround**: Images should render properly when published, or edit in Substack's web interface
- **Status**: High priority - investigating python-substack library's captioned_image() method

### 4. Blockquote Styling
- **Issue**: Blockquotes display with `>` prefix instead of styled quote blocks
- **Impact**: Quotes appear as plain text with markdown syntax
- **Workaround**: Edit in Substack's web interface after publishing
- **Status**: Requires deeper integration with Substack's block format

### 5. Rate Limiting
- **Issue**: No rate limiting implemented
- **Impact**: Rapid API calls might trigger Substack's undocumented rate limits
- **Workaround**: Use tools responsibly with reasonable delays between operations
- **Status**: Planned for future release

### 6. Limited Post Types
- **Issue**: No support for collaborative posts, threads, or podcasts
- **Impact**: Can only create standard posts
- **Status**: Outside current scope

### 7. Analytics Access
- **Issue**: No access to post analytics or subscriber data beyond count
- **Impact**: Cannot retrieve views, opens, or engagement metrics
- **Status**: Limitation of available API endpoints

### 8. Subscriber Count Shows Zero
- **Issue**: get_subscriber_count may show 0 even when you have subscribers
- **Impact**: Incorrect subscriber count displayed
- **Cause**: The python-substack library's API methods may not return accurate counts for newer or smaller publications
- **Workaround**: Check subscriber count directly in Substack's dashboard
- **Status**: Investigating - appears to be an API limitation

### 9. Post Scheduling Not Supported (Tool Removed)
- **Issue**: schedule_post was removed from the tool set due to consistent 404 API errors
- **Impact**: Cannot schedule posts via the MCP tools
- **Cause**: The python-substack library uses an outdated or incorrect API endpoint that returns 404 errors even when scheduling is available in the web interface
- **Workaround**: Schedule posts through Substack's web interface
- **Status**: Feature removed in v1.0.3 - python-substack library hasn't been updated in 2+ years

### 10. Shareable Preview Links Not Supported
- **Issue**: Unable to generate shareable preview links for draft posts
- **Impact**: Authors cannot share drafts for feedback before publishing
- **Current Workaround**: Tool generates author-only preview links in format:
  - `https://publication.substack.com/publish/post/{post_id}?back=%2Fpublish%2Fposts%2Fdrafts`
  - These links only work when logged in as the author
  - Cannot be shared with others for feedback
- **Root Cause**: Substack's shareable preview URLs use a UUID that differs from the post ID, and the python-substack library doesn't provide access to this UUID
- **Status**: Known limitation - requires deeper API investigation or library updates

## Technical Limitations

### API Limitations
Since Substack does not provide an official public API, we rely on reverse-engineered endpoints which may:
- Change without notice
- Have undocumented rate limits
- Behave differently than expected
- Not support all features available in the web interface

### Authentication Limitations
- Session tokens expire and need refreshing
- CAPTCHA challenges may appear during high usage
- Some accounts with advanced security settings may have issues

### Content Limitations
- Maximum post size limits are undocumented
- Some special characters may not render correctly
- Embedded content (tweets, videos) must be added manually
- No support for custom CSS or JavaScript

## Reporting New Issues

If you discover an issue not listed here:

1. Check existing [GitHub Issues](https://github.com/ty13r/substack-mcp-plus/issues)
2. Create a new issue using our bug report template
3. Include:
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Error messages (if any)
   - Your environment details

## Workaround Strategies

### For Formatting Issues
1. Create your draft with our tools
2. Use Substack's web editor for final formatting touches
3. Preview before publishing

### For Complex Posts
1. Use our tools for basic structure and content
2. Add advanced features (embeds, custom formatting) via web interface
3. Schedule publication through our tools after web edits

## Future Improvements

We're actively working on:
- Better text formatting support
- Improved error messages
- Rate limiting implementation
- Enhanced blockquote and list handling

Track progress in our [GitHub Issues](https://github.com/ty13r/substack-mcp-plus/issues).