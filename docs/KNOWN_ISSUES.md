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

### 3. Blockquote Styling
- **Issue**: Blockquotes display with `>` prefix instead of styled quote blocks
- **Impact**: Quotes appear as plain text with markdown syntax
- **Workaround**: Edit in Substack's web interface after publishing
- **Status**: Requires deeper integration with Substack's block format

### 4. Rate Limiting
- **Issue**: No rate limiting implemented
- **Impact**: Rapid API calls might trigger Substack's undocumented rate limits
- **Workaround**: Use tools responsibly with reasonable delays between operations
- **Status**: Planned for future release

### 5. Limited Post Types
- **Issue**: No support for collaborative posts, threads, or podcasts
- **Impact**: Can only create standard posts
- **Status**: Outside current scope

### 6. Analytics Access
- **Issue**: No access to post analytics or subscriber data beyond count
- **Impact**: Cannot retrieve views, opens, or engagement metrics
- **Status**: Limitation of available API endpoints

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